import difflib
import os
import re
import shlex
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
import pytesseract


FRAME_TEMPLATES_DIR = Path(__file__).resolve().parent / 'frame_templates'
DEFAULT_TESSERACT_WINDOWS_PATH = Path(r'C:\Program Files\Tesseract-OCR\tesseract.exe')
NAME_SANITIZER = re.compile(r'[^a-z0-9]+')
LEVEL_REGEX = re.compile(r'(?:lv|l|v)?\s*[:.]?\s*(\d{1,2})', re.IGNORECASE)
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
FRAME_REGION_MATCH_THRESHOLD = 0.55
FRAME_CROP_MATCH_THRESHOLD = 0.45
FRAME_UPTIE_MATCH_THRESHOLD = 0.68


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
    image = cv2.imdecode(np_image, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError('Failed to decode image payload.')

    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    return image


def extract_card_regions(image):
    frame_regions = extract_frame_validated_regions(image)
    template_regions = extract_card_regions_from_templates(image)

    if len(frame_regions) >= max(4, len(template_regions)):
        return frame_regions

    if template_regions:
        return template_regions

    if frame_regions:
        return frame_regions

    return fallback_grid_regions(image)


def extract_frame_validated_regions(image):
    candidates = extract_contour_card_candidates(image)
    if not candidates:
        candidates = fallback_grid_regions(image)

    scored_candidates = []
    for x, y, width, height in candidates:
        card = image[y:y + height, x:x + width]
        _uptie_level, confidence = score_frame_templates(card)
        if confidence < FRAME_CROP_MATCH_THRESHOLD:
            continue
        scored_candidates.append((x, y, width, height, confidence))

    if not scored_candidates:
        return []

    deduped = []
    for candidate in sorted(scored_candidates, key=lambda item: item[4], reverse=True):
        if any(overlapping_regions(candidate[:4], existing[:4]) for existing in deduped):
            continue
        deduped.append(candidate)

    filtered = filter_to_dominant_card_size(deduped)
    return sorted([candidate[:4] for candidate in filtered[:24]], key=lambda item: (item[1], item[0]))


def extract_contour_card_candidates(image):
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
        return []

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


def extract_card_regions_from_templates(image):
    templates = load_frame_templates()
    if not templates:
        return []

    height, width = image.shape[:2]
    scale = 1600 / max(height, width) if max(height, width) > 1600 else 1.0
    working = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale != 1.0 else image.copy()
    grayscale = cv2.cvtColor(working, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (3, 3), 0)
    candidates = []

    for template in templates:
        for frame_scale in build_frame_scale_candidates(template['shape'], working.shape[:2]):
            scaled_width = int(template['shape'][1] * frame_scale)
            scaled_height = int(template['shape'][0] * frame_scale)

            if scaled_width >= working.shape[1] or scaled_height >= working.shape[0]:
                continue

            interpolation = cv2.INTER_AREA if frame_scale < 1.0 else cv2.INTER_CUBIC
            resized_template = cv2.resize(template['grayscale'], (scaled_width, scaled_height), interpolation=interpolation)
            resized_mask = cv2.resize(template['mask'], (scaled_width, scaled_height), interpolation=cv2.INTER_NEAREST)

            if np.count_nonzero(resized_mask) < 40:
                continue

            result = cv2.matchTemplate(blurred, resized_template, cv2.TM_CCORR_NORMED, mask=resized_mask)
            flat_scores = result.ravel()
            if not flat_scores.size:
                continue

            top_count = min(8, flat_scores.size)
            top_indices = np.argpartition(flat_scores, -top_count)[-top_count:]

            for index in top_indices:
                score = float(flat_scores[index])
                if score < FRAME_REGION_MATCH_THRESHOLD:
                    continue

                y, x = np.unravel_index(int(index), result.shape)
                candidates.append((int(x), int(y), scaled_width, scaled_height, score))

    if not candidates:
        return []

    deduped = []
    for candidate in sorted(candidates, key=lambda item: item[4], reverse=True)[:200]:
        box = candidate[:4]
        if any(overlapping_regions(box, existing[:4]) for existing in deduped):
            continue
        deduped.append(candidate)

    deduped = filter_to_dominant_card_size(deduped)

    restored = [
        (
            int(x / scale),
            int(y / scale),
            int(card_width / scale),
            int(card_height / scale),
        )
        for x, y, card_width, card_height, _score in deduped[:24]
    ]

    return sorted(restored, key=lambda item: (item[1], item[0]))


def filter_to_dominant_card_size(candidates):
    if len(candidates) <= 2:
        return candidates

    best_group = candidates
    best_group_score = -1.0

    for candidate in candidates:
        anchor_area = candidate[2] * candidate[3]
        lower_bound = anchor_area * 0.7
        upper_bound = anchor_area * 1.4
        group = [
            item for item in candidates
            if lower_bound <= (item[2] * item[3]) <= upper_bound
        ]
        group_score = sum(item[4] for item in group)

        if group_score > best_group_score:
            best_group = group
            best_group_score = group_score

    return best_group


def fallback_grid_regions(image):
    height, width = image.shape[:2]
    columns = 6 if width >= 900 else 3
    rows = 2 if height >= 500 else 1
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
    regions = [
        card[int(height * 0.56):int(height * 0.9), int(width * 0.44):width],
        card[int(height * 0.52):int(height * 0.88), int(width * 0.4):width],
        card[int(height * 0.58):int(height * 0.94), int(width * 0.48):width],
    ]

    for region in regions:
        for text in collect_ocr_candidates(region, psm=7, whitelist='LVlv0123456789.:'):
            match = LEVEL_REGEX.search(text)
            if match:
                return sanitize_level(match.group(1))

            digit_match = re.search(r'(\d{1,2})', text)
            if digit_match:
                return sanitize_level(digit_match.group(1))

    return 1


def extract_name(card):
    height, width = card.shape[:2]
    regions = [
        card[int(height * 0.42):int(height * 0.8), int(width * 0.08):int(width * 0.92)],
        card[int(height * 0.5):int(height * 0.87), int(width * 0.05):int(width * 0.95)],
        card[int(height * 0.6):int(height * 0.95), int(width * 0.06):int(width * 0.94)],
    ]
    best_text = ''
    best_score = -1

    for region in regions:
        for text in collect_ocr_candidates(
            region,
            psm=6,
            whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'/ :",
        ):
            score = score_identity_text(text)
            if score > best_score:
                best_score = score
                best_text = text

    return best_text


def collect_ocr_candidates(region, psm, whitelist=''):
    if region.size == 0:
        return []

    grayscale = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    enlarged = cv2.resize(grayscale, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    filtered = cv2.bilateralFilter(enlarged, 9, 75, 75)
    thresholded = [filtered]
    _, otsu = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, inverse_otsu = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    adaptive = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
    thresholded.extend([otsu, inverse_otsu, adaptive])

    config_parts = [f'--psm {psm}']
    if whitelist:
        config_parts.append(f'-c tessedit_char_whitelist={shlex.quote(whitelist)}')
    config = ' '.join(config_parts)
    candidates = []

    for variant in thresholded:
        text = ' '.join((pytesseract.image_to_string(variant, config=config) or '').split())
        if text and text not in candidates:
            candidates.append(text)

    return candidates


def score_identity_text(text):
    letters = len(re.findall(r'[A-Za-z]', text))
    digits = len(re.findall(r'\d', text))
    punctuation_noise = len(re.findall(r"[^A-Za-z0-9\s\-\.'/\":]", text))
    return (letters * 2.0) + min(digits, 3) - (punctuation_noise * 1.5)


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
    best_level, best_score = score_frame_templates(card)

    if best_level is None or best_score < FRAME_UPTIE_MATCH_THRESHOLD:
        return None, 0.0

    return best_level, best_score


def score_frame_templates(card):
    signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    best_level = None
    best_score = 0.0

    for template in load_frame_templates():
        resized_template = cv2.resize(template['grayscale'], (grayscale.shape[1], grayscale.shape[0]))
        score = cv2.matchTemplate(grayscale, resized_template, cv2.TM_CCOEFF_NORMED).max()

        if score > best_score:
            best_score = float(score)
            best_level = template['uptie_level']

    return best_level, best_score


@lru_cache(maxsize=1)
def load_frame_templates():
    templates = []

    for uptie_level in range(1, 5):
        template_dir = FRAME_TEMPLATES_DIR / f'uptie{uptie_level}'
        if not template_dir.exists():
            continue

        for template_path in sorted(template_dir.iterdir()):
            if template_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
            if template is None:
                continue

            signature = extract_frame_signature(template)
            grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(grayscale, 50, 150)
            mask = np.where(grayscale > 0, 255, 0).astype(np.uint8)

            if not np.count_nonzero(edges):
                continue

            templates.append(
                {
                    'uptie_level': uptie_level,
                    'grayscale': grayscale,
                    'edges': edges,
                    'mask': mask,
                    'shape': grayscale.shape,
                }
            )

    return tuple(templates)


def extract_frame_signature(card):
    height, width = card.shape[:2]
    border = max(4, int(min(height, width) * 0.09))
    signature = card.copy()
    signature[border:height - border, border:width - border] = 0
    return signature


def build_frame_scale_candidates(template_shape, image_shape):
    template_height, template_width = template_shape
    image_height, image_width = image_shape
    min_width = max(72, int(image_width * 0.08))
    max_width = min(max(int(image_width * 0.4), 160), image_width - 8)
    min_scale = max(0.35, min_width / float(template_width))
    max_scale = min(1.6, max_width / float(template_width))

    if min_scale > max_scale:
        return [max_scale]

    values = np.arange(min_scale, max_scale + 0.001, 0.08)
    scales = sorted({round(float(value), 2) for value in values} | {round(min_scale, 2), round(max_scale, 2), 1.0})
    return [scale for scale in scales if int(template_height * scale) < image_height and int(template_width * scale) < image_width]


def overlapping_regions(first_box, second_box):
    if intersection_over_union(first_box, second_box) > 0.35:
        return True

    if intersection_over_smaller_area(first_box, second_box) > 0.3:
        return True

    first_center_x = first_box[0] + (first_box[2] / 2.0)
    first_center_y = first_box[1] + (first_box[3] / 2.0)
    second_center_x = second_box[0] + (second_box[2] / 2.0)
    second_center_y = second_box[1] + (second_box[3] / 2.0)
    max_distance = min(first_box[2], second_box[2], first_box[3], second_box[3]) * 0.2

    return abs(first_center_x - second_center_x) <= max_distance and abs(first_center_y - second_center_y) <= max_distance


def intersection_over_smaller_area(first_box, second_box):
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
    smaller_area = min(first_width * first_height, second_width * second_height)
    return intersection_area / smaller_area if smaller_area else 0.0


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