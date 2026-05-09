import ast
import difflib
import io
import json
import os
import re
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor


FRAME_TEMPLATES_DIR = Path(__file__).resolve().parent / 'frame_templates'
NAME_SANITIZER = re.compile(r'[^a-z0-9]+')
LEVEL_REGEX = re.compile(r'(?:lv|l|v)?\s*[:.]?\s*(\d{1,2})', re.IGNORECASE)
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
FRAME_REGION_MATCH_THRESHOLD = 0.55
FRAME_CROP_MATCH_THRESHOLD = 0.45
FRAME_UPTIE_MATCH_THRESHOLD = 0.68
DEFAULT_QWEN_VL_MODEL = 'Qwen/Qwen3-VL-2B-Instruct'
QWEN_CARD_OCR_PROMPT = (
    'Read the game character card image and return strict JSON only. '
    'Use this exact schema: '
    '{"name":"", "level":"", "text":""}. '
    'Rules: '
    '1) `name` is the visible character or identity name only, without level text. '
    '2) `level` is the visible numeric level only, no prefix like Lv. '
    '3) `text` is a compact OCR transcription of the visible card text relevant to name and level. '
    '4) If a field is unreadable, use an empty string. '
    '5) Output JSON only and do not use markdown fences.'
)
RARITY_TEMPLATE_REGEX = re.compile(r'_(0{1,3})$', re.IGNORECASE)
LEVEL_OCR_REGIONS = (
    (0.44, 0.56, 1.0, 0.9),
    (0.4, 0.52, 1.0, 0.88),
    (0.48, 0.58, 1.0, 0.94),
)
NAME_OCR_REGIONS = (
    (0.12, 0.6, 0.9, 0.86),
    (0.08, 0.56, 0.94, 0.9),
    (0.06, 0.48, 0.95, 0.86),
    (0.18, 0.64, 0.92, 0.94),
)
KNOWN_OCR_LABELS = (
    'LCB Sinner',
    'Heishou Pack Wu Branch Adept',
    'Heishou Pack Mao Branch Adept',
    'Heishou Pack Wei Branch',
    'Heishou Pack Mao Branch',
    'The Ring Fauvist Student',
    'The Lord of Hongyuan',
    'Heishou Pack You Branch Adept',
    'Family Hierarch Candidate',
    'The Ring Fauvist Docent',
    'Heishou Pack You Branch',
    'The Ring Pointillist Student',
    'Heishou Pack Si Branch',
)


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


def normalize_rarity(value):
    if not value:
        return None

    normalized = str(value).strip()
    return normalized or None


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
            'name_tokens': tokenize_name(entry.get('name', '')),
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
        raw_name, detected_label, matched_entry, name_confidence = match_card_name(card, manifest)
        level = extract_level(card)
        uptie, uptie_confidence = infer_uptie(card, matched_entry)
        combined_confidence = round((name_confidence * 0.8) + (uptie_confidence * 0.2), 4)

        results.append(
            {
                'source_image': source_name,
                'bounds': {'x': int(x), 'y': int(y), 'width': int(width), 'height': int(height)},
                'ocr_name': detected_label or raw_name,
                'raw_ocr_name': raw_name,
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

    if len(frame_regions) >= 6:
        return frame_regions

    template_regions = extract_card_regions_from_templates(image)
    template_regions = expand_template_anchor_regions(template_regions, image)

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
        return []

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

    candidates = []

    for contour in extract_candidate_contours(working):
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


def extract_candidate_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 80, 180)
    edge_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    edge_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, edge_kernel, iterations=2)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gold_mask = cv2.inRange(hsv, (10, 80, 140), (45, 255, 255))
    red_mask = cv2.inRange(hsv, (0, 90, 110), (10, 255, 255)) + cv2.inRange(hsv, (170, 90, 110), (180, 255, 255))
    color_mask = cv2.bitwise_or(gold_mask, red_mask)
    color_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    color_closed = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, color_kernel, iterations=2)
    color_closed = cv2.dilate(color_closed, color_kernel, iterations=1)

    contours = []
    for binary in (edge_closed, color_closed):
        found, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.extend(found)

    return contours


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


def expand_template_anchor_regions(regions, image):
    filtered_regions = filter_template_anchor_regions(regions, image.shape[:2])
    if len(filtered_regions) < 3:
        return filtered_regions

    rows = group_regions_by_rows(filtered_regions)
    expanded = [(*region, 1.0) for region in filtered_regions]
    image_height, image_width = image.shape[:2]
    global_x_positions = sorted({region[0] for region in filtered_regions})

    for row in rows:
        if not row:
            continue

        median_width = int(np.median([region[2] for region in row]))
        median_height = int(np.median([region[3] for region in row]))
        median_y = int(np.median([region[1] for region in row]))
        step = estimate_region_step(row, median_width)
        existing_x = sorted(region[0] for region in row)

        predicted_x_positions = set(existing_x)
        predicted_x_positions.update(fill_missing_row_positions(existing_x, step))
        predicted_x_positions.update(global_x_positions)
        current_x = existing_x[0]
        while current_x - step >= int(image_width * 0.14):
            current_x -= step
            predicted_x_positions.add(int(round(current_x)))

        current_x = existing_x[-1]
        while current_x + step + median_width <= int(image_width * 0.86):
            current_x += step
            predicted_x_positions.add(int(round(current_x)))

        for x in sorted(predicted_x_positions):
            candidate_box = (int(x), median_y, median_width, median_height)
            if any(intersection_over_union(candidate_box, existing[:4]) > 0.4 for existing in expanded):
                continue

            x1 = max(0, candidate_box[0])
            y1 = max(0, candidate_box[1])
            x2 = min(image_width, candidate_box[0] + candidate_box[2])
            y2 = min(image_height, candidate_box[1] + candidate_box[3])

            if x2 <= x1 or y2 <= y1:
                continue

            card = image[y1:y2, x1:x2]
            _uptie, confidence = score_frame_templates(card)
            if confidence < max(FRAME_REGION_MATCH_THRESHOLD, 0.5):
                continue

            expanded.append((x1, y1, x2 - x1, y2 - y1, confidence))

    deduped = []
    for candidate in sorted(expanded, key=lambda item: item[4], reverse=True):
        if any(overlapping_regions(candidate[:4], existing[:4]) for existing in deduped):
            continue
        deduped.append(candidate)

    return sorted([candidate[:4] for candidate in deduped], key=lambda item: (item[1], item[0]))


def filter_template_anchor_regions(regions, image_shape):
    image_height, image_width = image_shape
    filtered = []

    for x, y, width, height in regions:
        center_x = x + (width / 2.0)
        center_y = y + (height / 2.0)

        if center_x < image_width * 0.14 or center_x > image_width * 0.86:
            continue

        if center_y < image_height * 0.1 or center_y > image_height * 0.85:
            continue

        filtered.append((x, y, width, height))

    return filtered


def group_regions_by_rows(regions):
    rows = []

    for region in sorted(regions, key=lambda item: item[1]):
        center_y = region[1] + (region[3] / 2.0)
        matched_row = None

        for row in rows:
            row_center = np.median([item[1] + (item[3] / 2.0) for item in row])
            if abs(center_y - row_center) <= np.median([item[3] for item in row]) * 0.45:
                matched_row = row
                break

        if matched_row is None:
            rows.append([region])
        else:
            matched_row.append(region)

    return [sorted(row, key=lambda item: item[0]) for row in rows]


def estimate_region_step(row, default_width):
    steps = []

    for left, right in zip(row, row[1:]):
        delta = right[0] - left[0]
        if default_width * 0.75 <= delta <= default_width * 1.5:
            steps.append(delta)

    if steps:
        return int(round(float(np.median(steps))))

    return int(round(default_width * 1.04))


def fill_missing_row_positions(existing_x, step):
    inferred_positions = set()

    for left_x, right_x in zip(existing_x, existing_x[1:]):
        gap = right_x - left_x
        if gap <= step * 1.6:
            continue

        missing_count = max(0, int(round(gap / float(step))) - 1)
        for index in range(1, missing_count + 1):
            inferred_positions.add(int(round(left_x + (step * index))))

    return inferred_positions


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
    for text in collect_card_ocr_candidates(card, LEVEL_OCR_REGIONS, whitelist='LVlv0123456789.:'):
        match = LEVEL_REGEX.search(text)
        if match:
            return sanitize_level(match.group(1))

        digit_match = re.search(r'(\d{1,2})', text)
        if digit_match:
            return sanitize_level(digit_match.group(1))

    return 1


def extract_name(card):
    candidates = extract_name_candidates(card)
    return candidates[0] if candidates else ''


def extract_name_candidates(card):
    ranked_candidates = []

    for text in collect_card_ocr_candidates(
        card,
        NAME_OCR_REGIONS,
        whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'/ :",
    ):
        score = score_identity_text(text)
        ranked_candidates.append((score, text))

    ranked_candidates.sort(key=lambda item: item[0], reverse=True)
    deduped = []

    for _score, text in ranked_candidates:
        if text not in deduped:
            deduped.append(text)

    return deduped


def match_card_name(card, manifest):
    best_text = ''
    best_label = ''
    best_entry = None
    best_score = 0.0

    for candidate in extract_name_candidates(card):
        matched_entry, score = match_manifest_entry(candidate, manifest)
        detected_label = normalize_detected_label(candidate, matched_entry, score, manifest)

        if score > best_score:
            best_text = candidate
            best_label = detected_label
            best_entry = matched_entry
            best_score = score

    if best_text:
        return best_text, best_label, best_entry, best_score

    raw_name = extract_name(card)
    matched_entry, score = match_manifest_entry(raw_name, manifest)
    return raw_name, normalize_detected_label(raw_name, matched_entry, score, manifest), matched_entry, score


def collect_card_ocr_candidates(card, normalized_regions, whitelist=''):
    candidates = []
    seen = set()
    ocr_result = extract_card_ocr_result(card)

    raw_candidates = []
    if ocr_result.get('level'):
        raw_candidates.append(ocr_result['level'])
        raw_candidates.append(f"Lv {ocr_result['level']}")

    raw_candidates.extend(
        [
            ocr_result.get('name', ''),
            strip_level_prefix(ocr_result.get('text', '')),
            ocr_result.get('text', ''),
            ocr_result.get('raw_output', ''),
        ]
    )

    for text in raw_candidates:
        candidate = filter_ocr_text(text, whitelist)
        if candidate and candidate not in seen:
            seen.add(candidate)
            candidates.append(candidate)

    return candidates


def filter_ocr_text(text, whitelist=''):
    normalized = normalize_ocr_text(text)
    if not normalized:
        return ''

    if not whitelist:
        return normalized

    allowed_characters = set(whitelist)
    filtered = ''.join(character for character in normalized if character in allowed_characters or character.isspace())
    return ' '.join(filtered.split())


def extract_card_ocr_result(card):
    image_bytes = encode_png_bytes(card)
    return run_qwen_card_ocr(image_bytes)


def encode_png_bytes(image):
    success, encoded = cv2.imencode('.png', image)
    if not success:
        raise ValueError('Failed to encode image payload for OCR.')

    return encoded.tobytes()


@lru_cache(maxsize=96)
def run_qwen_card_ocr(image_bytes):
    try:
        output_text = generate_qwen_card_ocr(image_bytes)
    except Exception as exc:
        raise RuntimeError(f'Qwen3-VL OCR request failed: {exc}') from exc

    return parse_qwen_card_ocr_output(output_text)


def generate_qwen_card_ocr(image_bytes):
    model, processor = get_qwen_vl_components()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'image'},
                {'type': 'text', 'text': QWEN_CARD_OCR_PROMPT},
            ],
        }
    ]
    prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[prompt], images=[image], return_tensors='pt')
    device = get_qwen_vl_device(model)
    inputs = {key: value.to(device) if hasattr(value, 'to') else value for key, value in inputs.items()}

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=int(os.environ.get('QWEN_VL_MAX_NEW_TOKENS', '192')),
            do_sample=False,
        )

    trimmed_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs['input_ids'], generated_ids)]
    return processor.batch_decode(trimmed_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]


@lru_cache(maxsize=1)
def get_qwen_vl_components():
    model_name = os.environ.get('QWEN_VL_MODEL', DEFAULT_QWEN_VL_MODEL)
    model_kwargs = {
        'torch_dtype': resolve_qwen_torch_dtype(),
        'low_cpu_mem_usage': True,
    }

    if torch.cuda.is_available():
        model_kwargs['device_map'] = 'auto'

    try:
        processor = AutoProcessor.from_pretrained(model_name)
        model = AutoModelForImageTextToText.from_pretrained(model_name, **model_kwargs)
    except Exception as exc:
        raise RuntimeError(f'Failed to load Qwen3-VL model `{model_name}`: {exc}') from exc

    if not torch.cuda.is_available():
        model = model.to('cpu')

    model.eval()
    return model, processor


def warm_qwen_model():
    get_qwen_vl_components()


def get_qwen_vl_device(model):
    return next(model.parameters()).device


def resolve_qwen_torch_dtype():
    configured = os.environ.get('QWEN_VL_DTYPE', 'auto').strip().lower()
    if configured == 'float32':
        return torch.float32
    if configured == 'float16':
        return torch.float16
    if configured == 'bfloat16':
        return torch.bfloat16

    return torch.float16 if torch.cuda.is_available() else torch.float32


def parse_qwen_card_ocr_output(output_text):
    normalized_output = normalize_ocr_text(output_text)
    payload = extract_json_object(output_text)

    name = normalize_ocr_text(str(payload.get('name', '') or '')) if payload else ''
    level = normalize_ocr_text(str(payload.get('level', '') or '')) if payload else ''
    text = normalize_ocr_text(str(payload.get('text', '') or '')) if payload else ''

    if not text:
        text = normalized_output

    if not name:
        name = strip_level_prefix(text)

    level_match = LEVEL_REGEX.search(level) or LEVEL_REGEX.search(text)
    if level_match:
        level = level_match.group(1)
    else:
        digit_match = re.search(r'(\d{1,2})', level) or re.search(r'(\d{1,2})', text)
        level = digit_match.group(1) if digit_match else ''

    return {
        'name': name,
        'level': level,
        'text': text,
        'raw_output': normalized_output,
    }


def extract_json_object(text):
    match = re.search(r'\{.*\}', str(text), flags=re.DOTALL)
    if not match:
        return None

    candidate = match.group(0)
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(candidate)
        except (SyntaxError, ValueError):
            return None

    return parsed if isinstance(parsed, dict) else None


def score_identity_text(text):
    letters = len(re.findall(r'[A-Za-z]', text))
    digits = len(re.findall(r'\d', text))
    punctuation_noise = len(re.findall(r"[^A-Za-z0-9\s\-\.'/\":]", text))
    return (letters * 2.0) + min(digits, 3) - (punctuation_noise * 1.5)


def normalize_ocr_text(text):
    return ' '.join(text.replace('\n', ' ').replace('|', 'I').split())


def tokenize_name(text):
    return tuple(re.findall(r'[a-z0-9]+', str(text).lower()))


def normalize_detected_label(raw_name, matched_entry, match_score, manifest):
    lower_text = raw_name.lower()
    if 'lcb' in lower_text and ('sinner' in lower_text or 'siener' in lower_text or 'simmer' in lower_text):
        return 'LCB Sinner'

    if matched_entry and match_score >= 0.82 and matched_entry['entryKey'].startswith('LCB Sinner'):
        return 'LCB Sinner'

    label_candidates = list(KNOWN_OCR_LABELS)
    label_candidates.extend(entry['name'] for entry in manifest if entry.get('name'))

    cleaned_text = strip_level_prefix(raw_name)
    best_label = cleaned_text or raw_name
    best_score = 0.0

    for label in label_candidates:
        candidate_score = fuzzy_label_score(cleaned_text or raw_name, label)
        if candidate_score > best_score:
            best_score = candidate_score
            best_label = label

    if best_score >= 0.72:
        if best_label.startswith('LCB Sinner'):
            return 'LCB Sinner'
        return best_label

    if matched_entry and match_score >= 0.72:
        if matched_entry['entryKey'].startswith('LCB Sinner'):
            return 'LCB Sinner'
        return matched_entry['entryKey']

    return cleaned_text or raw_name


def strip_level_prefix(text):
    cleaned = re.sub(r'\bL[vVyYwW][.:]?\s*\d{1,2}\b', ' ', str(text), flags=re.IGNORECASE)
    cleaned = re.sub(r'\b\d{1,2}\b', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(" -.:')(")
    return cleaned


def fuzzy_label_score(left_text, right_text):
    normalized_left = sanitize_name(left_text)
    normalized_right = sanitize_name(right_text)
    if not normalized_left or not normalized_right:
        return 0.0

    base_score = difflib.SequenceMatcher(None, normalized_left, normalized_right).ratio()
    partial_score = partial_ratio(normalized_left, normalized_right)
    token_score = overlap_score(tokenize_name(left_text), tokenize_name(right_text))
    return (max(base_score, partial_score) * 0.75) + (token_score * 0.25)


def match_manifest_entry(raw_name, manifest):
    normalized_input = sanitize_name(raw_name)
    input_tokens = tokenize_name(raw_name)
    best_entry = None
    best_score = 0.0

    if not normalized_input:
        return None, 0.0

    for entry in manifest:
        candidate = entry['normalized_name']
        if not candidate:
            continue

        ratio = difflib.SequenceMatcher(None, normalized_input, candidate).ratio()
        partial = partial_ratio(normalized_input, candidate)
        token_bonus = overlap_score(input_tokens, entry['name_tokens'])
        containment_bonus = 1.0 if normalized_input in candidate or candidate in normalized_input else 0.0
        score = (max(ratio, partial) * 0.65) + (token_bonus * 0.25) + (containment_bonus * 0.1)

        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score < 0.4:
        return None, best_score

    return {
        'sinnerKey': best_entry['sinnerKey'],
        'category': best_entry['category'],
        'entryKey': best_entry['entryKey'],
        'rarity': normalize_rarity(best_entry.get('rarity')),
        'hasLevel': best_entry['hasLevel'],
    }, best_score


def overlap_score(left_tokens, right_tokens):
    left_chunks = set(left_tokens)
    right_chunks = set(right_tokens)

    if not left_chunks or not right_chunks:
        return 0.0

    return len(left_chunks & right_chunks) / len(left_chunks | right_chunks)


def partial_ratio(left_text, right_text):
    shorter, longer = sorted((left_text, right_text), key=len)

    if not shorter or not longer:
        return 0.0

    if shorter in longer:
        return 1.0

    window = len(shorter)
    best = 0.0

    for start_index in range(0, max(1, len(longer) - window + 1)):
        chunk = longer[start_index:start_index + window]
        best = max(best, difflib.SequenceMatcher(None, shorter, chunk).ratio())
        if best >= 0.995:
            break

    return best


def infer_uptie(card, matched_entry=None):
    rarity = normalize_rarity((matched_entry or {}).get('rarity'))
    template_level, template_confidence = match_frame_templates(card, rarity=rarity)
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


def match_frame_templates(card, rarity=None):
    best_level, best_score = score_frame_templates(card, rarity=rarity)

    if best_level is None or best_score < FRAME_UPTIE_MATCH_THRESHOLD:
        return None, 0.0

    return best_level, best_score


def score_frame_templates(card, rarity=None):
    signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(signature, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    edges = cv2.Canny(grayscale, 50, 150)
    best_level = None
    best_score = 0.0

    for template in load_scaled_frame_templates(grayscale.shape[0], grayscale.shape[1]):
        if rarity and template['rarity'] and template['rarity'] != rarity:
            continue

        grayscale_score = cv2.matchTemplate(grayscale, template['grayscale'], cv2.TM_CCOEFF_NORMED).max()
        edge_score = cv2.matchTemplate(edges, template['edges'], cv2.TM_CCORR_NORMED).max()
        saturation_score = cv2.matchTemplate(saturation, template['saturation'], cv2.TM_CCOEFF_NORMED).max()
        value_score = cv2.matchTemplate(value, template['value'], cv2.TM_CCOEFF_NORMED).max()
        score = (
            (float(grayscale_score) * 0.45)
            + (float(edge_score) * 0.3)
            + (float(saturation_score) * 0.15)
            + (float(value_score) * 0.1)
        )

        if score > best_score:
            best_score = score
            best_level = template['uptie_level']

    return best_level, best_score


@lru_cache(maxsize=24)
def load_scaled_frame_templates(target_height, target_width):
    scaled_templates = []

    for template in load_frame_templates():
        scaled_templates.append(
            {
                'uptie_level': template['uptie_level'],
                'rarity': template['rarity'],
                'grayscale': cv2.resize(template['grayscale'], (target_width, target_height)),
                'edges': cv2.resize(template['edges'], (target_width, target_height), interpolation=cv2.INTER_NEAREST),
                'saturation': cv2.resize(template['saturation'], (target_width, target_height)),
                'value': cv2.resize(template['value'], (target_width, target_height)),
            }
        )

    return tuple(scaled_templates)


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
            hsv = cv2.cvtColor(signature, cv2.COLOR_BGR2HSV)
            edges = cv2.Canny(grayscale, 50, 150)
            mask = np.where(grayscale > 0, 255, 0).astype(np.uint8)

            if not np.count_nonzero(edges):
                continue

            templates.append(
                {
                    'uptie_level': uptie_level,
                    'rarity': parse_template_rarity(template_path),
                    'grayscale': grayscale,
                    'edges': edges,
                    'saturation': hsv[:, :, 1],
                    'value': hsv[:, :, 2],
                    'mask': mask,
                    'shape': grayscale.shape,
                }
            )

    return tuple(templates)


def parse_template_rarity(template_path):
    match = RARITY_TEMPLATE_REGEX.search(template_path.stem)
    if not match:
        return None

    return f'Rarity{match.group(1)}'


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