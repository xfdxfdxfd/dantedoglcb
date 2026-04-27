import difflib
import os
import re
from pathlib import Path

import cv2
import numpy as np
import pytesseract


FRAME_TEMPLATES_DIR = Path(__file__).resolve().parent / 'frame_templates'
DEFAULT_TESSERACT_WINDOWS_PATH = Path(r'C:\Program Files\Tesseract-OCR\tesseract.exe')
NAME_SANITIZER = re.compile(r'[^a-z0-9]+')
LEVEL_REGEX = re.compile(r'(?:lv|l|v)?\s*[:.]?\s*(\d{1,2})', re.IGNORECASE)


if os.environ.get('TESSERACT_CMD'):
    pytesseract.pytesseract.tesseract_cmd = os.environ['TESSERACT_CMD']
elif os.name == 'nt' and DEFAULT_TESSERACT_WINDOWS_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(DEFAULT_TESSERACT_WINDOWS_PATH)


def sanitize_name(text):
    return NAME_SANITIZER.sub('', text.lower())


def sanitize_level(value):
    try:
        return max(1, min(int(value), 50))
    except (TypeError, ValueError):
        return 1


def sanitize_uptie(value):
    try:
        return str(max(0, min(int(value), 4)))
    except (TypeError, ValueError):
        return '0'


def merge_updates_into_progress(progress, updates):
    merged = progress.copy()

    for update in updates:
        sinner_group = merged.get(update['sinnerKey'])
        if not sinner_group:
            continue

        category_group = sinner_group.get(update['category'])
        if not category_group:
            continue

        target_entry = category_group.get(update['entryKey'])
        if not target_entry:
            continue

        target_entry['uptied'] = sanitize_uptie(update.get('uptied'))
        if update['category'] == 'IDs' and update.get('level') is not None:
            target_entry['level'] = sanitize_level(update['level'])

    return merged


def recognize_screenshots_payload(images, roster_manifest):
    manifest = [
        {
            **entry,
            'normalized_name': sanitize_name(entry.get('name', '')),
        }
        for entry in roster_manifest
    ]

    updates_by_key = {}
    all_cards = []

    for uploaded_file in images:
        image_bytes = uploaded_file.read()
        cards = recognize_single_screenshot(image_bytes, uploaded_file.name, manifest)

        for card in cards:
            all_cards.append(card)

            matched_entry = card.get('matched_entry')
            if not matched_entry:
                continue

            update_key = (
                matched_entry['sinnerKey'],
                matched_entry['category'],
                matched_entry['entryKey'],
            )

            existing = updates_by_key.get(update_key)
            if existing and existing['confidence'] >= card['confidence']:
                continue

            update = {
                'sinnerKey': matched_entry['sinnerKey'],
                'category': matched_entry['category'],
                'entryKey': matched_entry['entryKey'],
                'uptied': card['uptie'],
                'level': card['level'] if matched_entry.get('hasLevel') else None,
                'confidence': round(card['confidence'], 4),
                'source_image': card['source_image'],
            }

            updates_by_key[update_key] = update

    updates = sorted(updates_by_key.values(), key=lambda item: item['confidence'], reverse=True)

    return {
        'processed_screenshots': len(images),
        'updates': updates,
        'cards': all_cards,
    }


def recognize_single_screenshot(image_bytes, source_name, manifest):
    image = decode_image(image_bytes)
    regions = extract_card_regions(image)
    results = []

    for bounds in regions:
        x, y, width, height = bounds
        card = image[y:y + height, x:x + width]
        raw_name = extract_name(card)
        matched_entry, name_confidence = match_manifest_entry(raw_name, manifest)
        level = extract_level(card)
        uptie, uptie_confidence = infer_uptie(card)
        combined_confidence = round((name_confidence * 0.8) + (uptie_confidence * 0.2), 4)

        results.append(
            {
                'source_image': source_name,
                'bounds': {'x': int(x), 'y': int(y), 'width': int(width), 'height': int(height)},
                'ocr_name': raw_name,
                'level': level,
                'uptie': uptie,
                'confidence': combined_confidence,
                'matched_entry': matched_entry,
            }
        )

    return results


def decode_image(image_bytes):
    np_image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError('Failed to decode image payload.')

    return image


def extract_card_regions(image):
    height, width = image.shape[:2]
    scale = 1600 / max(height, width) if max(height, width) > 1600 else 1.0
    working = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale != 1.0 else image.copy()

    gray = cv2.cvtColor(working, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 80, 180)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []

    for contour in contours:
        x, y, card_width, card_height = cv2.boundingRect(contour)
        area = card_width * card_height
        ratio = card_width / float(card_height)

        if area < working.shape[0] * working.shape[1] * 0.01:
            continue

        if not 0.45 <= ratio <= 0.9:
            continue

        candidates.append((x, y, card_width, card_height))

    if not candidates:
        return fallback_grid_regions(image)

    deduped = []
    for candidate in sorted(candidates, key=lambda item: item[2] * item[3], reverse=True):
        if any(intersection_over_union(candidate, existing) > 0.35 for existing in deduped):
            continue
        deduped.append(candidate)

    restored = [
        (
            int(x / scale),
            int(y / scale),
            int(card_width / scale),
            int(card_height / scale),
        )
        for x, y, card_width, card_height in deduped[:24]
    ]

    return sorted(restored, key=lambda item: (item[1], item[0]))


def fallback_grid_regions(image):
    height, width = image.shape[:2]
    columns = 6 if width >= 1200 else 3
    rows = 2 if height >= 700 else 1
    card_width = int(width / columns * 0.82)
    card_height = int(card_width * 1.4)
    x_gap = int(width / columns)
    y_gap = int(min(card_height * 1.08, height / max(rows, 1)))
    top_offset = int(height * 0.03)
    regions = []

    for row_index in range(rows):
        for column_index in range(columns):
            x = int(column_index * x_gap + (x_gap - card_width) / 2)
            y = int(top_offset + row_index * y_gap)
            if y + card_height <= height:
                regions.append((x, y, card_width, card_height))

    return regions


def extract_level(card):
    height, width = card.shape[:2]
    region = card[int(height * 0.58):int(height * 0.92), int(width * 0.48):width]
    grayscale = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    enlarged = cv2.resize(grayscale, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    _, thresholded = cv2.threshold(enlarged, 170, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(
        thresholded,
        config='--psm 7 -c tessedit_char_whitelist=LVlv0123456789.:',
    )
    match = LEVEL_REGEX.search(text or '')

    if match:
        return sanitize_level(match.group(1))

    digit_match = re.search(r'(\d{1,2})', text or '')
    if digit_match:
        return sanitize_level(digit_match.group(1))

    return 1


def extract_name(card):
    height, width = card.shape[:2]
    region = card[int(height * 0.5):int(height * 0.87), int(width * 0.05):int(width * 0.95)]
    grayscale = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    enlarged = cv2.resize(grayscale, None, fx=2.4, fy=2.4, interpolation=cv2.INTER_CUBIC)
    filtered = cv2.bilateralFilter(enlarged, 9, 75, 75)
    _, thresholded = cv2.threshold(filtered, 145, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresholded, config='--psm 6')
    return ' '.join((text or '').split())


def match_manifest_entry(raw_name, manifest):
    normalized_input = sanitize_name(raw_name)
    best_entry = None
    best_score = 0.0

    if not normalized_input:
        return None, 0.0

    for entry in manifest:
        candidate = entry['normalized_name']
        if not candidate:
            continue

        ratio = difflib.SequenceMatcher(None, normalized_input, candidate).ratio()
        token_bonus = overlap_score(normalized_input, candidate)
        score = (ratio * 0.75) + (token_bonus * 0.25)

        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score < 0.4:
        return None, best_score

    return {
        'sinnerKey': best_entry['sinnerKey'],
        'category': best_entry['category'],
        'entryKey': best_entry['entryKey'],
        'hasLevel': best_entry['hasLevel'],
    }, best_score


def overlap_score(left_text, right_text):
    left_chunks = set(re.findall(r'[a-z]+|\d+', left_text))
    right_chunks = set(re.findall(r'[a-z]+|\d+', right_text))

    if not left_chunks or not right_chunks:
        return 0.0

    return len(left_chunks & right_chunks) / len(left_chunks | right_chunks)


def infer_uptie(card):
    template_level, template_confidence = match_frame_templates(card)
    if template_level is not None:
        return template_level, template_confidence

    border_signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(border_signature, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale, 80, 200)
    edge_density = float(np.count_nonzero(edges)) / float(edges.size)

    hsv = cv2.cvtColor(border_signature, cv2.COLOR_BGR2HSV)
    gold_mask = cv2.inRange(hsv, (10, 90, 90), (40, 255, 255))
    red_mask = cv2.inRange(hsv, (0, 90, 70), (10, 255, 255)) + cv2.inRange(hsv, (170, 90, 70), (180, 255, 255))
    gold_ratio = float(np.count_nonzero(gold_mask)) / float(gold_mask.size)
    red_ratio = float(np.count_nonzero(red_mask)) / float(red_mask.size)

    if edge_density > 0.22 or gold_ratio > 0.30:
        return 4, 0.48
    if edge_density > 0.16 or gold_ratio > 0.22:
        return 3, 0.42
    if red_ratio > 0.18 or edge_density > 0.11:
        return 2, 0.36
    return 1, 0.32


def match_frame_templates(card):
    signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    best_level = None
    best_score = 0.0

    for uptie_level in range(1, 5):
        template_dir = FRAME_TEMPLATES_DIR / f'uptie{uptie_level}'
        if not template_dir.exists():
            continue

        for template_path in template_dir.iterdir():
            if template_path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
                continue

            template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
            if template is None:
                continue

            resized_template = cv2.resize(template, (grayscale.shape[1], grayscale.shape[0]))
            score = cv2.matchTemplate(grayscale, resized_template, cv2.TM_CCOEFF_NORMED).max()

            if score > best_score:
                best_score = float(score)
                best_level = uptie_level

    if best_level is None or best_score < 0.72:
        return None, 0.0

    return best_level, best_score


def extract_frame_signature(card):
    height, width = card.shape[:2]
    border = max(4, int(min(height, width) * 0.09))
    signature = card.copy()
    signature[border:height - border, border:width - border] = 0
    return signature


def intersection_over_union(first_box, second_box):
    first_x1, first_y1, first_width, first_height = first_box
    second_x1, second_y1, second_width, second_height = second_box
    first_x2 = first_x1 + first_width
    first_y2 = first_y1 + first_height
    second_x2 = second_x1 + second_width
    second_y2 = second_y1 + second_height

    intersection_x1 = max(first_x1, second_x1)
    intersection_y1 = max(first_y1, second_y1)
    intersection_x2 = min(first_x2, second_x2)
    intersection_y2 = min(first_y2, second_y2)

    if intersection_x2 <= intersection_x1 or intersection_y2 <= intersection_y1:
        return 0.0

    intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)
    first_area = first_width * first_height
    second_area = second_width * second_height
    union = first_area + second_area - intersection_area
    return intersection_area / union if union else 0.0