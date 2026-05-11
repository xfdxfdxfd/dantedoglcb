import base64
import ast
import copy
import difflib
import hashlib
import io
import json
import os
import re
import time
from functools import lru_cache
from pathlib import Path
from threading import Lock

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor


FRAME_TEMPLATES_DIR = Path(__file__).resolve().parent / 'frame_templates'
IDENTITY_ICON_TEMPLATES_DIR = Path(__file__).resolve().parent / 'identityIcon_templates'
OCR_FEEDBACK_PATH = Path(__file__).resolve().parent / 'ocr_feedback.json'
OCR_FEEDBACK_SAMPLES_DIR = Path(__file__).resolve().parent / 'ocr_feedback_samples'
NAME_SANITIZER = re.compile(r'[^a-z0-9]+')
LEVEL_REGEX = re.compile(r'(?:lv|l|v)?\s*[:.]?\s*(\d{1,2})', re.IGNORECASE)
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
FRAME_REGION_MATCH_THRESHOLD = 0.55
FRAME_CROP_MATCH_THRESHOLD = 0.45
FRAME_UPTIE_MATCH_THRESHOLD = 0.58
FRAME_UPTIE_MATCH_THRESHOLD_WITH_RARITY = 0.42
FRAME_UPTIE_MIN_MARGIN = 0.035
CARD_REGION_EDGE_MARGIN_RATIO = 0.05
FEEDBACK_SAMPLE_MIN_SCORE = 0.72
FEEDBACK_SAMPLE_MIN_MARGIN = 0.035
FEEDBACK_TEXT_PROFILE_LIMIT = 48
FEEDBACK_EXAMPLE_LIMIT = 96
ICON_MATCH_STRONG_SCORE_THRESHOLD = 0.36
ICON_MATCH_WEAK_SCORE_THRESHOLD = 0.26
ICON_MATCH_STRONG_MARGIN = 0.045
ICON_MATCH_TOP_K = 3
ALIAS_MATCH_EXACT_BONUS = 0.08
AMBIGUOUS_MATCH_SCORE_MARGIN = 0.035
MANIFEST_TOKEN_STOPWORDS = {
    'assoc', 'association', 'section', 'south', 'north', 'east', 'west', 'director',
    'office', 'fixer', 'corp', 'agent', 'sinner', 'pack', 'branch', 'student', 'adept',
    'manager', 'captain', 'first', 'mate', 'assistant', 'chief', 'butler', 'family',
    'workshop', 'cleanup', 'class', 'grade', 'the', 'of', 'and', 'lcb', 'yi', 'sang',
    'hong', 'lu', 'don', 'quixote', 'meursault', 'faust', 'ryoshu', 'heathcliff',
    'ishmael', 'rodion', 'sinclair', 'outis', 'gregor',
}
DEFAULT_QWEN_VL_MODEL = 'Qwen/Qwen3-VL-2B-Instruct'
QWEN_CARD_OCR_PROMPT = (
    'Inspect the labeled panels of one game identity card. '
    'The panel labeled CARD is the full card. '
    'The panel labeled NAME MAIN is a raw zoom of the identity title area. '
    'The panel labeled NAME ALT is a contrast-enhanced zoom of the same identity title area. '
    'The panel labeled SINNER ICON is a zoom of the top-right sinner icon. '
    'The panel labeled LEVEL is a zoom of the level number. '
    'Return exactly four lines in this exact format with no markdown, no prose, and no extra keys: '
    'NAME: <identity name>\n'
    'SINNER: <sinner name only>\n'
    'LEVEL: <integer level only>\n'
    'TEXT: <short supporting OCR text>. '
    'Rules: '
    '1) NAME must contain only the identity name and must not include Lv, level numbers, NEW, rarity marks, or labels. '
    '2) SINNER must contain only the sinner name, such as Yi Sang, Faust, Don Quixote, Hong Lu, or Ryoshu. '
    '3) LEVEL must contain digits only. '
    '4) TEXT may contain other visible card text that supports the read. '
    '5) If unreadable, leave the value empty after the colon. '
    '6) Do not invent words or numbers that are not visible in the image. '
    '7) Many titles share words like Assoc., South, and Section. Preserve the first distinctive faction or title word exactly as shown. '
    '8) Do not repeat the identity title or the sinner name twice.'
)
QWEN_CARD_UPTIE_PROMPT = (
    'Inspect the labeled panels of one game identity card frame. '
    'The first two panels are the real card corners: CARD TOP RIGHT and CARD BOTTOM LEFT. '
    'The next panels are two template candidates labeled C1 and C2. '
    'Each candidate shows the same two corners from a possible matching template. '
    'Choose which candidate matches the real card corners better. '
    'Return exactly one line in this exact format with no markdown, no prose, and no extra keys: '
    'CHOICE: C1 or CHOICE: C2. '
    'Rules: '
    '1) Return only C1 or C2. '
    '2) Compare ornament shape, border style, and corner details only. '
    '3) Ignore rarity pips and any text. '
    '4) If uncertain, still choose the closer of C1 or C2.'
)
QWEN_CARD_NAME_CHOICE_PROMPT = (
    'Inspect the labeled panels of one game identity card. '
    'The first panels show the real card, title area, sinner icon, and level area. '
    'The later panels labeled C1, C2, C3, and C4 are candidate identity names. '
    'Choose the candidate whose full identity name best matches the visible card title and sinner icon. '
    'Return exactly one line in this exact format with no markdown, no prose, and no extra keys: '
    'CHOICE: C1 or CHOICE: C2 or CHOICE: C3 or CHOICE: C4. '
    'Rules: '
    '1) Use the visible title text first. '
    '2) Pay special attention to the first distinctive word in the title because many candidates share suffixes like Assoc., South, and Section. '
    '3) Use the sinner icon only as a tie-breaker. '
    '4) Ignore uptie pips, frame decorations, and level numbers except when needed to reject a bad option. '
    '5) If uncertain, still choose the closest of the listed candidates.'
)
RARITY_TEMPLATE_REGEX = re.compile(r'_(0{1,3})$', re.IGNORECASE)
QWEN_TAGGED_FIELD_REGEX = re.compile(
    r'(name|sinner|level|text)\s*[:=-]\s*(.*?)\s*(?=(?:name|sinner|level|text)\s*[:=-]|$)',
    re.IGNORECASE | re.DOTALL,
)
QWEN_UPTIE_CHOICE_REGEX = re.compile(r'choice\s*[:=-]\s*(c[12])', re.IGNORECASE)
QWEN_NAME_CHOICE_REGEX = re.compile(r'choice\s*[:=-]\s*(c[1-4])', re.IGNORECASE)
QWEN_PANEL_WIDTH = 360
QWEN_PANEL_LABEL_HEIGHT = 34
QWEN_PANEL_GAP = 12
QWEN_NAME_MAIN_REGION = (0.08, 0.56, 0.94, 0.88)
QWEN_NAME_ALT_REGION = (0.06, 0.48, 0.95, 0.9)
QWEN_NAME_FOCUS_REGION = (0.14, 0.58, 0.94, 0.84)
QWEN_SINNER_ICON_REGION = (0.54, 0.0, 0.98, 0.26)
QWEN_LEVEL_REGION = (0.4, 0.5, 1.0, 0.9)
QWEN_UPTIE_TOP_RIGHT_REGION = (0.62, 0.0, 1.0, 0.28)
QWEN_UPTIE_BOTTOM_LEFT_REGION = (0.0, 0.72, 0.38, 1.0)
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
KNOWN_OCR_LABEL_RARITIES = {
    'LCB Sinner': 'Rarity0',
    'Heishou Pack Wu Branch Adept': 'Rarity000',
    'Heishou Pack Mao Branch Adept': 'Rarity000',
    'Heishou Pack Wei Branch': 'Rarity000',
    'Heishou Pack Mao Branch': 'Rarity000',
    'The Ring Fauvist Student': 'Rarity000',
    'The Lord of Hongyuan': 'Rarity000',
    'Heishou Pack You Branch Adept': 'Rarity000',
    'Family Hierarch Candidate': 'Rarity000',
    'The Ring Fauvist Docent': 'Rarity000',
    'Heishou Pack You Branch': 'Rarity000',
    'The Ring Pointillist Student': 'Rarity00',
    'Heishou Pack Si Branch': 'Rarity000',
}
IDENTITY_ICON_REGIONS = (
    (0.52, 0.0, 1.0, 0.3),
    (0.32, 0.0, 0.86, 0.3),
    (0.58, 0.0, 1.0, 0.24),
    (0.4, 0.0, 0.84, 0.24),
)
IDENTITY_ICON_SCALE_RATIOS = (0.58, 0.68, 0.78, 0.88)
SINNER_ICON_ALIASES = {
    'DonQuixote': ('Don', 'DonQuixote'),
    'Faust': ('Faust',),
    'Gregor': ('Gregor',),
    'Heathcliff': ('Heathcliff',),
    'HongLu': ('HongLu',),
    'Ishmael': ('Ishmael',),
    'Meursault': ('Meursault',),
    'Outis': ('Outis',),
    'Rodion': ('Rodion',),
    'Ryoshu': ('Ryoshu',),
    'Sinclair': ('Sinclair',),
    'YiSang': ('YiSang',),
}
OCR_FEEDBACK_LOCK = Lock()
DEFAULT_QWEN_OCR_MAX_NEW_TOKENS = 80
DEFAULT_QWEN_CHOICE_MAX_NEW_TOKENS = 12


def sanitize_name(text):
    return NAME_SANITIZER.sub('', text.lower())


def log_recognition_timing(stage, **fields):
    payload = ' '.join(f'{key}={value}' for key, value in fields.items())
    print(f'[recognition] {stage} {payload}'.strip(), flush=True)


def canonical_feedback_entry_key(sinner_key, category, entry_key):
    return f'{sinner_key}::{category}::{entry_key}'


def normalize_feedback_alias(text):
    cleaned = cleanup_identity_name(text)
    if cleaned:
        return cleaned

    normalized = normalize_ocr_text(text)
    return strip_level_prefix(normalized)


def trim_feedback_text(text):
    return ' '.join(str(text or '').split())


def sanitize_feedback_confidence(value):
    try:
        return round(max(0.0, min(float(value), 1.0)), 4)
    except (TypeError, ValueError):
        return 0.0


def normalize_feedback_text_profile(profile):
    if not isinstance(profile, dict):
        return None

    observed_name = normalize_feedback_alias(profile.get('observed_name', ''))
    raw_ocr_name = normalize_feedback_alias(profile.get('raw_ocr_name', ''))
    ocr_support_text = cleanup_identity_name(profile.get('ocr_support_text') or profile.get('support_text', ''))
    ocr_sinner_hint = normalize_qwen_sinner_hint(profile.get('ocr_sinner_hint') or profile.get('sinner_hint', ''))

    if not any((observed_name, raw_ocr_name, ocr_support_text, ocr_sinner_hint)):
        return None

    return {
        'observed_name': observed_name,
        'raw_ocr_name': raw_ocr_name,
        'ocr_support_text': ocr_support_text,
        'ocr_sinner_hint': ocr_sinner_hint,
        'saved_at': int(profile.get('saved_at') or 0),
    }


def feedback_text_profile_key(profile):
    return (
        profile.get('observed_name', ''),
        profile.get('raw_ocr_name', ''),
        profile.get('ocr_support_text', ''),
        profile.get('ocr_sinner_hint', ''),
    )


def normalize_feedback_example_record(example):
    if not isinstance(example, dict):
        return None

    input_payload = example.get('input') if isinstance(example.get('input'), dict) else {}
    target_payload = example.get('target') if isinstance(example.get('target'), dict) else {}
    entry_key = trim_feedback_text(target_payload.get('entry_key') or target_payload.get('entryKey') or '')
    if not entry_key:
        return None

    return {
        'image_path': trim_feedback_text(example.get('image_path') or ''),
        'input': {
            'observed_name': trim_feedback_text(input_payload.get('observed_name') or ''),
            'raw_ocr_name': trim_feedback_text(input_payload.get('raw_ocr_name') or ''),
            'ocr_support_text': trim_feedback_text(input_payload.get('ocr_support_text') or ''),
            'ocr_sinner_hint': trim_feedback_text(input_payload.get('ocr_sinner_hint') or ''),
            'recognition_confidence': sanitize_feedback_confidence(input_payload.get('recognition_confidence') or 0.0),
            'source_image': trim_feedback_text(input_payload.get('source_image') or ''),
            'manual': bool(input_payload.get('manual')),
        },
        'target': {
            'sinner_key': trim_feedback_text(target_payload.get('sinner_key') or target_payload.get('sinnerKey') or ''),
            'category': trim_feedback_text(target_payload.get('category') or ''),
            'entry_key': entry_key,
            'canonical_name': trim_feedback_text(target_payload.get('canonical_name') or target_payload.get('canonicalName') or entry_key),
            'visible_name': trim_feedback_text(target_payload.get('visible_name') or target_payload.get('visibleName') or entry_key),
        },
        'saved_at': int(example.get('saved_at') or 0),
    }


def feedback_example_key(example):
    return json.dumps(
        {
            'image_path': example.get('image_path', ''),
            'input': example.get('input', {}),
            'target': example.get('target', {}),
        },
        sort_keys=True,
        ensure_ascii=True,
    )


def normalize_manifest_entry(entry, feedback_store=None):
    feedback = feedback_store if feedback_store is not None else load_ocr_feedback_store()
    feedback_entry = feedback.get(canonical_feedback_entry_key(entry.get('sinnerKey'), entry.get('category'), entry.get('entryKey')), {})
    aliases = []
    for alias in feedback_entry.get('aliases', []):
        normalized_alias = normalize_feedback_alias(alias)
        if normalized_alias and normalized_alias not in aliases:
            aliases.append(normalized_alias)

    return {
        **entry,
        'normalized_name': sanitize_name(entry.get('name', '')),
        'name_tokens': tokenize_name(entry.get('name', '')),
        'match_aliases': tuple(aliases),
        'match_alias_tokens': tuple(tokenize_name(alias) for alias in aliases),
        'feedback_samples': tuple(feedback_entry.get('samples', [])),
        'feedback_text_profiles': tuple(feedback_entry.get('text_profiles', [])),
    }


def load_ocr_feedback_store():
    if not OCR_FEEDBACK_PATH.exists():
        return {}

    try:
        payload = json.loads(OCR_FEEDBACK_PATH.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(payload, dict):
        return {}

    normalized = {}
    for entry_key, entry_payload in payload.items():
        if not isinstance(entry_payload, dict):
            continue

        aliases = []
        for alias in entry_payload.get('aliases', []):
            normalized_alias = normalize_feedback_alias(alias)
            if normalized_alias and normalized_alias not in aliases:
                aliases.append(normalized_alias)

        text_profiles = []
        seen_profile_keys = set()
        for profile in entry_payload.get('text_profiles', []):
            normalized_profile = normalize_feedback_text_profile(profile)
            if not normalized_profile:
                continue
            profile_key = feedback_text_profile_key(normalized_profile)
            if profile_key in seen_profile_keys:
                continue
            seen_profile_keys.add(profile_key)
            text_profiles.append(normalized_profile)

        examples = []
        seen_example_keys = set()
        for example in entry_payload.get('examples', []):
            normalized_example = normalize_feedback_example_record(example)
            if not normalized_example:
                continue
            example_key = feedback_example_key(normalized_example)
            if example_key in seen_example_keys:
                continue
            seen_example_keys.add(example_key)
            examples.append(normalized_example)

        if aliases or text_profiles or entry_payload.get('samples') or examples:
            normalized[entry_key] = {
                'aliases': aliases,
                'raw_aliases': list(entry_payload.get('raw_aliases', [])),
                'samples': list(entry_payload.get('samples', [])),
                'text_profiles': text_profiles,
                'examples': examples,
            }

    return normalized


def save_ocr_feedback_store(payload):
    OCR_FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    OCR_FEEDBACK_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding='utf-8')


def sanitize_feedback_path_component(text):
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '-', str(text or '').strip())
    return cleaned.strip('.-') or 'sample'


def decode_feedback_image_data_url(data_url):
    if not isinstance(data_url, str):
        return None, None

    match = re.match(r'^data:image/(?P<format>png|jpeg|jpg|webp);base64,(?P<data>.+)$', data_url, flags=re.IGNORECASE)
    if not match:
        return None, None

    try:
        image_bytes = base64.b64decode(match.group('data'))
    except (ValueError, TypeError):
        return None, None

    image_format = match.group('format').lower().replace('jpeg', 'jpg')
    return image_bytes, image_format


def save_feedback_sample_image(feedback_key, corrected_text, image_data_url):
    image_bytes, image_format = decode_feedback_image_data_url(image_data_url)
    if not image_bytes or not image_format:
        return ''

    entry_directory = OCR_FEEDBACK_SAMPLES_DIR / sanitize_feedback_path_component(feedback_key)
    entry_directory.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(image_bytes + corrected_text.encode('utf-8')).hexdigest()[:24]
    sample_path = entry_directory / f'{digest}.{image_format}'

    if not sample_path.exists():
        sample_path.write_bytes(image_bytes)

    return sample_path.relative_to(OCR_FEEDBACK_PATH.parent).as_posix()


def build_feedback_sample_record(item, feedback_key, entry_key):
    corrected_text = ' '.join(str(item.get('corrected_text') or entry_key).split())
    image_path = save_feedback_sample_image(feedback_key, corrected_text, item.get('card_image_data_url'))
    if not image_path:
        return None

    bounds = item.get('bounds') or {}
    return {
        'image_path': image_path,
        'corrected_text': corrected_text,
        'observed_name': ' '.join(str(item.get('observed_name') or '').split()),
        'raw_ocr_name': ' '.join(str(item.get('raw_ocr_name') or '').split()),
        'ocr_support_text': ' '.join(str(item.get('ocr_support_text') or '').split()),
        'ocr_sinner_hint': ' '.join(str(item.get('ocr_sinner_hint') or '').split()),
        'recognition_confidence': sanitize_feedback_confidence(item.get('recognition_confidence') or 0.0),
        'source_image': ' '.join(str(item.get('source_image') or '').split()),
        'bounds': {
            'x': int(bounds.get('x') or 0),
            'y': int(bounds.get('y') or 0),
            'width': int(bounds.get('width') or 0),
            'height': int(bounds.get('height') or 0),
        },
        'manual': bool(item.get('manual')),
        'saved_at': int(time.time()),
    }


def build_feedback_text_profile_record(item):
    return normalize_feedback_text_profile(
        {
            'observed_name': item.get('observed_name', ''),
            'raw_ocr_name': item.get('raw_ocr_name', ''),
            'ocr_support_text': item.get('ocr_support_text', ''),
            'ocr_sinner_hint': item.get('ocr_sinner_hint', ''),
            'saved_at': int(time.time()),
        }
    )


def build_feedback_example_record(item, entry, sample_record=None):
    entry_key = trim_feedback_text((entry or {}).get('entryKey') or '')
    if not entry_key:
        return None

    corrected_text = trim_feedback_text(item.get('corrected_text') or entry_key)
    return {
        'image_path': (sample_record or {}).get('image_path', ''),
        'input': {
            'observed_name': trim_feedback_text(item.get('observed_name') or ''),
            'raw_ocr_name': trim_feedback_text(item.get('raw_ocr_name') or ''),
            'ocr_support_text': trim_feedback_text(item.get('ocr_support_text') or ''),
            'ocr_sinner_hint': trim_feedback_text(item.get('ocr_sinner_hint') or ''),
            'recognition_confidence': sanitize_feedback_confidence(item.get('recognition_confidence') or 0.0),
            'source_image': trim_feedback_text(item.get('source_image') or ''),
            'manual': bool(item.get('manual')),
        },
        'target': {
            'sinner_key': trim_feedback_text((entry or {}).get('sinnerKey') or ''),
            'category': trim_feedback_text((entry or {}).get('category') or ''),
            'entry_key': entry_key,
            'canonical_name': entry_key,
            'visible_name': corrected_text or entry_key,
        },
        'saved_at': int(time.time()),
    }


def store_recognition_feedback(feedback_items):
    persisted = 0

    with OCR_FEEDBACK_LOCK:
        existing = load_ocr_feedback_store()

        for item in feedback_items:
            entry = item.get('entry') or {}
            sinner_key = entry.get('sinnerKey')
            category = entry.get('category')
            entry_key = entry.get('entryKey')
            if not sinner_key or not category or not entry_key:
                continue

            aliases = []
            for candidate in (item.get('observed_name'), item.get('raw_ocr_name')):
                normalized_alias = normalize_feedback_alias(candidate)
                if normalized_alias:
                    aliases.append(normalized_alias)

            feedback_key = canonical_feedback_entry_key(sinner_key, category, entry_key)
            feedback_entry = existing.setdefault(feedback_key, {'aliases': [], 'raw_aliases': [], 'samples': [], 'text_profiles': [], 'examples': []})
            known_aliases = list(feedback_entry.get('aliases', []))
            known_raw_aliases = list(feedback_entry.get('raw_aliases', []))
            known_samples = list(feedback_entry.get('samples', []))
            known_text_profiles = list(feedback_entry.get('text_profiles', []))
            known_examples = list(feedback_entry.get('examples', []))
            changed = False

            for alias in aliases:
                if alias == entry_key or alias in known_aliases:
                    continue
                known_aliases.append(alias)
                changed = True

            for candidate in (item.get('observed_name'), item.get('raw_ocr_name')):
                raw_alias = ' '.join(str(candidate or '').split())
                if not raw_alias or raw_alias in known_raw_aliases:
                    continue
                known_raw_aliases.append(raw_alias)
                changed = True

            sample_record = build_feedback_sample_record(item, feedback_key, entry_key)
            if sample_record and not any(existing_sample.get('image_path') == sample_record['image_path'] for existing_sample in known_samples):
                known_samples.append(sample_record)
                changed = True

            text_profile = build_feedback_text_profile_record(item)
            if text_profile:
                text_profile_key = feedback_text_profile_key(text_profile)
                if not any(feedback_text_profile_key(existing_profile) == text_profile_key for existing_profile in known_text_profiles):
                    known_text_profiles.append(text_profile)
                    changed = True

            example_record = build_feedback_example_record(item, entry, sample_record=sample_record)
            if example_record:
                example_identity = feedback_example_key(example_record)
                if not any(feedback_example_key(existing_example) == example_identity for existing_example in known_examples):
                    known_examples.append(example_record)
                    changed = True

            if not aliases and not sample_record and not text_profile and not example_record:
                continue

            if changed:
                feedback_entry['aliases'] = known_aliases[-24:]
                feedback_entry['raw_aliases'] = known_raw_aliases[-24:]
                feedback_entry['samples'] = known_samples[-24:]
                feedback_entry['text_profiles'] = known_text_profiles[-FEEDBACK_TEXT_PROFILE_LIMIT:]
                feedback_entry['examples'] = known_examples[-FEEDBACK_EXAMPLE_LIMIT:]
                persisted += 1

        if persisted:
            save_ocr_feedback_store(existing)

    return persisted


def sanitize_level(value):
    try:
        return max(1, min(int(value), 60))
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
    started_at = time.perf_counter()
    manifest_started_at = time.perf_counter()
    feedback_store = load_ocr_feedback_store()
    manifest = [normalize_manifest_entry(entry, feedback_store=feedback_store) for entry in roster_manifest]
    manifest_elapsed = time.perf_counter() - manifest_started_at

    updates_by_key = {}
    all_cards = []

    for uploaded_file in images:
        file_started_at = time.perf_counter()
        image_bytes = uploaded_file.read()
        cards = recognize_single_screenshot(image_bytes, uploaded_file.name, manifest)
        log_recognition_timing(
            'screenshot',
            name=uploaded_file.name,
            cards=len(cards),
            seconds=f'{time.perf_counter() - file_started_at:.3f}',
        )

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
    log_recognition_timing(
        'batch',
        images=len(images),
        cards=len(all_cards),
        manifest_entries=len(manifest),
        manifest_seconds=f'{manifest_elapsed:.3f}',
        total_seconds=f'{time.perf_counter() - started_at:.3f}',
    )

    return {
        'processed_screenshots': len(images),
        'updates': updates,
        'cards': all_cards,
    }


def recognize_single_screenshot(image_bytes, source_name, manifest):
    screenshot_started_at = time.perf_counter()
    decode_started_at = time.perf_counter()
    image = decode_image(image_bytes)
    decode_elapsed = time.perf_counter() - decode_started_at
    region_started_at = time.perf_counter()
    regions = extract_card_regions(image)
    region_elapsed = time.perf_counter() - region_started_at
    results = []

    for index, bounds in enumerate(regions, start=1):
        card_started_at = time.perf_counter()
        x, y, width, height = bounds
        card = image[y:y + height, x:x + width]
        ocr_started_at = time.perf_counter()
        ocr_result = extract_card_ocr_result(card)
        ocr_elapsed = time.perf_counter() - ocr_started_at
        match_started_at = time.perf_counter()
        raw_name, detected_label, matched_entry, name_confidence = match_card_name(card, manifest, ocr_result=ocr_result)
        match_elapsed = time.perf_counter() - match_started_at
        level_started_at = time.perf_counter()
        level = extract_level(card, ocr_result=ocr_result)
        level_elapsed = time.perf_counter() - level_started_at
        uptie_started_at = time.perf_counter()
        uptie, uptie_confidence = infer_uptie(card, matched_entry, detected_label or raw_name)
        uptie_elapsed = time.perf_counter() - uptie_started_at
        combined_confidence = round((name_confidence * 0.8) + (uptie_confidence * 0.2), 4)
        log_recognition_timing(
            'card',
            image=source_name,
            index=index,
            ocr_seconds=f'{ocr_elapsed:.3f}',
            match_seconds=f'{match_elapsed:.3f}',
            level_seconds=f'{level_elapsed:.3f}',
            uptie_seconds=f'{uptie_elapsed:.3f}',
            total_seconds=f'{time.perf_counter() - card_started_at:.3f}',
            matched=bool(matched_entry),
        )

        results.append(
            {
                'source_image': source_name,
                'bounds': {'x': int(x), 'y': int(y), 'width': int(width), 'height': int(height)},
                'ocr_name': detected_label or raw_name,
                'raw_ocr_name': raw_name,
                'ocr_support_text': ocr_result.get('text', ''),
                'ocr_sinner_hint': ocr_result.get('sinner', ''),
                'level': level,
                'uptie': uptie,
                'confidence': combined_confidence,
                'matched_entry': matched_entry,
            }
        )

    log_recognition_timing(
        'regions',
        image=source_name,
        decode_seconds=f'{decode_elapsed:.3f}',
        region_seconds=f'{region_elapsed:.3f}',
        cards=len(results),
        total_seconds=f'{time.perf_counter() - screenshot_started_at:.3f}',
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
        return rescue_missing_grid_regions(image, frame_regions)

    template_regions = extract_card_regions_from_templates(image)
    template_regions = expand_template_anchor_regions(template_regions, image)

    if len(frame_regions) >= max(4, len(template_regions)):
        return rescue_missing_grid_regions(image, frame_regions)

    if template_regions:
        return rescue_missing_grid_regions(image, template_regions)

    if frame_regions:
        return rescue_missing_grid_regions(image, frame_regions)

    return rescue_missing_grid_regions(image, fallback_grid_regions(image))


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

    is_sparse_layout = len(filtered_regions) <= 6
    rows = group_regions_by_rows(filtered_regions)
    expanded = [(*region, 1.0) for region in filtered_regions]
    image_height, image_width = image.shape[:2]
    target_columns = 6 if image_width >= 900 else 3
    min_center_x = image_width * CARD_REGION_EDGE_MARGIN_RATIO
    max_center_x = image_width * (1.0 - CARD_REGION_EDGE_MARGIN_RATIO)
    global_x_positions = sorted({region[0] for region in filtered_regions})
    global_step = estimate_global_region_step(filtered_regions) if is_sparse_layout else None

    for row in rows:
        if not row:
            continue
        if len(row) >= target_columns:
            continue

        median_width = int(np.median([region[2] for region in row]))
        median_height = int(np.median([region[3] for region in row]))
        median_y = int(np.median([region[1] for region in row]))
        step = estimate_region_step(row, median_width)
        if is_sparse_layout and len(row) < 3 and global_step:
            step = global_step
        existing_x = sorted(region[0] for region in row)
        added_to_row = len(row)

        predicted_x_positions = set(existing_x)
        predicted_x_positions.update(fill_missing_row_positions(existing_x, step))
        predicted_x_positions.update(global_x_positions)
        current_x = existing_x[0]
        while (current_x - step + (median_width / 2.0)) >= min_center_x:
            current_x -= step
            predicted_x_positions.add(int(round(current_x)))

        current_x = existing_x[-1]
        while (current_x + step + (median_width / 2.0)) <= max_center_x:
            current_x += step
            predicted_x_positions.add(int(round(current_x)))

        for x in sorted(predicted_x_positions):
            if added_to_row >= target_columns:
                break

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
            threshold = FRAME_CROP_MATCH_THRESHOLD if is_sparse_layout else max(FRAME_REGION_MATCH_THRESHOLD, 0.5)
            if confidence < threshold:
                continue

            expanded.append((x1, y1, x2 - x1, y2 - y1, confidence))
            added_to_row += 1

    deduped = []
    for candidate in sorted(expanded, key=lambda item: item[4], reverse=True):
        if any(overlapping_regions(candidate[:4], existing[:4]) for existing in deduped):
            continue
        deduped.append(candidate)

    return sorted([candidate[:4] for candidate in deduped], key=lambda item: (item[1], item[0]))


def filter_template_anchor_regions(regions, image_shape):
    image_height, image_width = image_shape
    min_center_x = image_width * CARD_REGION_EDGE_MARGIN_RATIO
    max_center_x = image_width * (1.0 - CARD_REGION_EDGE_MARGIN_RATIO)
    filtered = []

    for x, y, width, height in regions:
        center_x = x + (width / 2.0)
        center_y = y + (height / 2.0)

        if center_x < min_center_x or center_x > max_center_x:
            continue

        if center_y < image_height * 0.08 or center_y > image_height * 0.95:
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


def estimate_global_region_step(regions):
    if len(regions) < 3:
        return None

    median_width = float(np.median([region[2] for region in regions]))
    sorted_x = sorted({region[0] for region in regions})
    steps = []

    for left_x, right_x in zip(sorted_x, sorted_x[1:]):
        delta = right_x - left_x
        if median_width * 0.75 <= delta <= median_width * 1.5:
            steps.append(delta)

    if not steps:
        return None

    return int(round(float(np.median(steps))))


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
    rows = 3 if height >= 850 else 2 if height >= 500 else 1
    card_width = int(width / columns * 0.82)
    card_height = int(card_width * 1.4)
    x_gap = int(width / columns)
    top_offset = int(height * 0.03)
    regions = []

    if rows == 1:
        y_positions = [top_offset]
    else:
        bottom_offset = int(height * 0.03)
        max_y = max(top_offset, height - card_height - bottom_offset)
        y_positions = [int(round(value)) for value in np.linspace(top_offset, max_y, rows)]

    for y in y_positions:
        for column_index in range(columns):
            x = int(column_index * x_gap + (x_gap - card_width) / 2)
            if y + card_height <= height:
                regions.append((x, y, card_width, card_height))

    return regions


def infer_grid_regions_from_detected(image, regions):
    if not regions:
        return fallback_grid_regions(image)

    image_height, image_width = image.shape[:2]
    expected_rows = 3 if image_height >= 850 else 2 if image_height >= 500 else 1
    rows = [row for row in group_regions_by_rows(regions) if row]

    if not rows:
        return fallback_grid_regions(image)

    column_count = max(len(row) for row in rows)
    if column_count < 3:
        return fallback_grid_regions(image)

    full_rows = [row for row in rows if len(row) == column_count]
    reference_rows = full_rows or [row for row in rows if len(row) >= max(3, column_count - 1)]
    if not reference_rows:
        reference_rows = rows

    card_width = int(round(float(np.median([region[2] for row in reference_rows for region in row]))))
    card_height = int(round(float(np.median([region[3] for row in reference_rows for region in row]))))

    if card_width < 40 or card_height < 60:
        return fallback_grid_regions(image)

    if full_rows:
        x_positions = [
            int(round(float(np.median([row[column_index][0] for row in full_rows]))))
            for column_index in range(column_count)
        ]
    else:
        anchor_row = max(reference_rows, key=lambda row: (len(row), sum(region[2] for region in row)))
        x_positions = [region[0] for region in anchor_row]

    row_tops = [int(round(float(np.median([region[1] for region in row])))) for row in rows]
    row_tops = sorted(set(row_tops))

    if len(row_tops) >= 2:
        row_step = int(round(float(np.median([right - left for left, right in zip(row_tops, row_tops[1:])]))))
    else:
        row_step = int(round(card_height * 1.03))

    if row_step < int(card_height * 0.75):
        row_step = int(round(card_height * 1.03))

    while len(row_tops) < expected_rows:
        next_top = row_tops[-1] + row_step
        if next_top + card_height > image_height:
            break
        row_tops.append(next_top)

    inferred = []
    for top in row_tops:
        y = min(max(0, int(round(top))), max(0, image_height - card_height))
        for left in x_positions:
            x = min(max(0, int(round(left))), max(0, image_width - card_width))
            inferred.append((x, y, card_width, card_height))

    return sorted(inferred, key=lambda item: (item[1], item[0]))


def has_card_frame_border(card):
    if card is None or not card.size:
        return False

    height, width = card.shape[:2]
    if height < 40 or width < 30:
        return False

    hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    gold_mask = cv2.inRange(hsv, (8, 70, 120), (45, 255, 255))
    red_mask = cv2.inRange(hsv, (0, 90, 90), (12, 255, 255)) + cv2.inRange(hsv, (168, 90, 90), (180, 255, 255))
    frame_mask = cv2.bitwise_or(gold_mask, red_mask)

    edge_width = max(6, int(round(width * 0.08)))
    top_height = max(6, int(round(height * 0.08)))
    left_density = float(np.count_nonzero(frame_mask[:, :edge_width])) / float(height * edge_width)
    right_density = float(np.count_nonzero(frame_mask[:, width - edge_width:])) / float(height * edge_width)
    top_density = float(np.count_nonzero(frame_mask[:top_height, :])) / float(top_height * width)

    return (
        (left_density >= 0.045 and right_density >= 0.045)
        or (top_density >= 0.06 and max(left_density, right_density) >= 0.04)
    )


def rescue_missing_grid_regions(image, regions):
    if not regions:
        return regions

    grid_regions = infer_grid_regions_from_detected(image, regions)
    if len(grid_regions) <= len(regions) or len(regions) < 6:
        return sorted(regions, key=lambda item: (item[1], item[0]))

    rescued = list(regions)
    for candidate in grid_regions:
        if any(overlapping_regions(candidate, existing) for existing in rescued):
            continue

        x, y, card_width, card_height = candidate
        card = image[y:y + card_height, x:x + card_width]
        if not has_card_frame_border(card):
            continue

        _uptie_level, confidence = score_frame_templates(card)

        if confidence >= max(0.3, FRAME_CROP_MATCH_THRESHOLD - 0.12):
            rescued.append(candidate)
            continue

        if confidence < 0.22 or not is_visually_dense_card(card):
            continue

        if qwen_card_looks_like_identity(card):
            rescued.append(candidate)

    return sorted(rescued, key=lambda item: (item[1], item[0]))


def is_visually_dense_card(card):
    if card is None or not card.size:
        return False

    grayscale = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale, 50, 150)
    edge_density = float(np.count_nonzero(edges)) / float(edges.size)
    hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    saturation_mean = float(np.mean(hsv[:, :, 1])) / 255.0
    value_std = float(np.std(hsv[:, :, 2]))
    return edge_density >= 0.055 or (saturation_mean >= 0.16 and value_std >= 18.0)


def qwen_card_looks_like_identity(card):
    ocr_result = extract_card_ocr_result(card)
    name = cleanup_identity_name(ocr_result.get('name', ''))
    support_text = normalize_ocr_text(ocr_result.get('text', ''))
    letter_count = len(re.findall(r'[A-Za-z]', name))
    support_letters = len(re.findall(r'[A-Za-z]', support_text))
    token_count = len(tokenize_name(name))
    return bool(ocr_result.get('level')) and (
        (letter_count >= 8 and token_count >= 2)
        or (letter_count >= 12 and support_letters >= 8)
    )


def extract_level(card, ocr_result=None):
    for text in collect_card_ocr_candidates(card, LEVEL_OCR_REGIONS, whitelist='LVlv0123456789.:', ocr_result=ocr_result):
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


def extract_name_candidates(card, ocr_result=None):
    ranked_candidates = []

    if ocr_result is None:
        ocr_result = extract_card_ocr_result(card)

    for text in build_name_candidates_from_ocr_result(ocr_result):
        score = score_identity_text(text) + 4.0
        ranked_candidates.append((score, text))

    for text in collect_card_ocr_candidates(
        card,
        NAME_OCR_REGIONS,
        whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'/ :",
        ocr_result=ocr_result,
    ):
        score = score_identity_text(text)
        ranked_candidates.append((score, text))

    ranked_candidates.sort(key=lambda item: item[0], reverse=True)
    deduped = []

    for _score, text in ranked_candidates:
        if text not in deduped:
            deduped.append(text)

    return deduped


def build_name_candidates_from_ocr_result(ocr_result):
    candidates = []
    for key in ('name', 'tagged_name', 'text'):
        value = normalize_ocr_text(str((ocr_result or {}).get(key, '') or ''))
        if not value:
            continue
        cleaned = cleanup_identity_name(value)
        if cleaned:
            candidates.append(cleaned)
        candidates.append(value)
    return [candidate for candidate in candidates if candidate]


def match_card_name(card, manifest, ocr_result=None):
    if ocr_result is None:
        ocr_result = extract_card_ocr_result(card)
    name_candidates = extract_name_candidates(card, ocr_result=ocr_result)
    support_text = build_ocr_support_text(ocr_result)
    icon_matches = rank_identity_icon_matches(card)
    qwen_sinner_hint = normalize_qwen_sinner_hint(ocr_result.get('sinner', ''))
    icon_manifest = narrow_manifest_with_icon_hints(manifest, icon_matches, name_candidates, qwen_sinner_hint)
    best_text = ''
    best_label = ''
    best_entry = None
    best_score = 0.0

    for candidate in name_candidates:
        matched_entry, score = match_manifest_entry(candidate, icon_manifest, support_text=support_text)
        detected_label = normalize_detected_label(candidate, matched_entry, score, icon_manifest)

        if score > best_score:
            best_text = candidate
            best_label = detected_label
            best_entry = matched_entry
            best_score = score

    if icon_manifest is not manifest and (best_score < 0.72 or best_entry is None):
        fallback_text, fallback_label, fallback_entry, fallback_score = match_card_name_against_manifest(
            name_candidates,
            manifest,
            support_text=support_text,
        )
        if fallback_score >= best_score:
            return fallback_text, fallback_label, fallback_entry, fallback_score

    sample_choice_entry, sample_choice_score = choose_manifest_entry_with_feedback_samples(card, icon_manifest, best_score, best_entry)
    if sample_choice_entry:
        chosen_text = sample_choice_entry['entryKey']
        return chosen_text, chosen_text, sample_choice_entry, max(best_score, sample_choice_score)

    qwen_choice_entry = choose_manifest_entry_with_qwen(card, name_candidates, icon_manifest, best_score, best_entry, support_text=support_text)
    if qwen_choice_entry:
        return qwen_choice_entry['entryKey'], qwen_choice_entry['entryKey'], qwen_choice_entry, max(best_score, 0.78)

    if best_text:
        return best_text, best_label, best_entry, best_score

    raw_name = ocr_result.get('name') or extract_name(card)
    matched_entry, score = match_manifest_entry(raw_name, manifest, support_text=support_text)
    return raw_name, normalize_detected_label(raw_name, matched_entry, score, manifest), matched_entry, score


def match_card_name_against_manifest(name_candidates, manifest, support_text=''):
    best_text = ''
    best_label = ''
    best_entry = None
    best_score = 0.0

    for candidate in name_candidates:
        matched_entry, score = match_manifest_entry(candidate, manifest, support_text=support_text)
        detected_label = normalize_detected_label(candidate, matched_entry, score, manifest)

        if score > best_score:
            best_text = candidate
            best_label = detected_label
            best_entry = matched_entry
            best_score = score

    return best_text, best_label, best_entry, best_score


def narrow_manifest_with_icon_hints(manifest, icon_matches, name_candidates, qwen_sinner_hint=''):
    if not manifest:
        return manifest

    if qwen_sinner_hint:
        qwen_narrowed = [
            entry for entry in manifest
            if match_manifest_sinner_label(entry.get('sinnerKey'), {qwen_sinner_hint})
        ]
        if qwen_narrowed:
            manifest = qwen_narrowed

    if not icon_matches:
        return manifest

    ambiguous_name = is_ambiguous_name_candidate_set(name_candidates)
    top_score = icon_matches[0]['score']
    second_score = icon_matches[1]['score'] if len(icon_matches) > 1 else 0.0
    margin = top_score - second_score

    if top_score >= ICON_MATCH_STRONG_SCORE_THRESHOLD and margin >= ICON_MATCH_STRONG_MARGIN:
        allowed_labels = {icon_matches[0]['label']}
    elif ambiguous_name and top_score >= ICON_MATCH_WEAK_SCORE_THRESHOLD:
        allowed_labels = {
            match['label']
            for match in icon_matches[:ICON_MATCH_TOP_K]
            if (top_score - match['score']) <= 0.04
        }
    else:
        return manifest

    narrowed = [
        entry for entry in manifest
        if match_manifest_sinner_label(entry.get('sinnerKey'), allowed_labels)
    ]
    return narrowed or manifest


def normalize_qwen_sinner_hint(text):
    normalized_text = sanitize_name(text or '')
    if not normalized_text:
        return ''

    best_label = ''
    best_length = 0
    for label, aliases in SINNER_ICON_ALIASES.items():
        candidates = {label, *aliases}
        for candidate in candidates:
            normalized_candidate = sanitize_name(candidate)
            if not normalized_candidate:
                continue
            if normalized_text == normalized_candidate or normalized_candidate in normalized_text or normalized_text in normalized_candidate:
                if len(normalized_candidate) > best_length:
                    best_label = label
                    best_length = len(normalized_candidate)

    return best_label


def choose_manifest_entry_with_qwen(card, name_candidates, manifest, best_score, best_entry, support_text=''):
    candidate_entries = get_top_manifest_entry_candidates(name_candidates, manifest, limit=4, support_text=support_text)
    if len(candidate_entries) < 2:
        return None

    top_candidate_score = candidate_entries[0]['candidateScore']
    second_candidate_score = candidate_entries[1]['candidateScore'] if len(candidate_entries) > 1 else 0.0
    needs_qwen = best_entry is None or best_score < 0.86 or (top_candidate_score - second_candidate_score) < 0.05
    if not needs_qwen:
        return None

    choice = run_qwen_card_name_choice(encode_png_bytes(build_qwen_card_name_choice_image(card, candidate_entries)))
    if not choice:
        return None

    for index, entry in enumerate(candidate_entries, start=1):
        if choice == f'C{index}':
            return {
                'sinnerKey': entry['sinnerKey'],
                'category': entry['category'],
                'entryKey': entry['entryKey'],
                'rarity': normalize_rarity(entry.get('rarity')),
                'hasLevel': entry['hasLevel'],
            }

    return None


def choose_manifest_entry_with_feedback_samples(card, manifest, best_score, best_entry):
    if best_entry is not None and best_score >= 0.86:
        return None, 0.0

    entries_with_samples = [entry for entry in manifest if entry.get('feedback_samples')]
    if not entries_with_samples:
        return None, 0.0

    card_signature = build_feedback_sample_signature(card)
    best_sample_entry = None
    best_sample_score = 0.0
    second_best_score = 0.0

    for entry in entries_with_samples:
        entry_score = 0.0

        for sample in entry.get('feedback_samples') or ():
            sample_signature = load_feedback_sample_signature(sample.get('image_path', ''))
            if sample_signature is None:
                continue

            entry_score = max(entry_score, score_feedback_sample_signature(card_signature, sample_signature))

        if entry_score > best_sample_score:
            second_best_score = best_sample_score
            best_sample_score = entry_score
            best_sample_entry = entry
        elif entry_score > second_best_score:
            second_best_score = entry_score

    if best_sample_entry is None:
        return None, 0.0

    if best_sample_score < FEEDBACK_SAMPLE_MIN_SCORE:
        return None, best_sample_score

    if (best_sample_score - second_best_score) < FEEDBACK_SAMPLE_MIN_MARGIN:
        return None, best_sample_score

    return {
        'sinnerKey': best_sample_entry['sinnerKey'],
        'category': best_sample_entry['category'],
        'entryKey': best_sample_entry['entryKey'],
        'rarity': normalize_rarity(best_sample_entry.get('rarity')),
        'hasLevel': best_sample_entry['hasLevel'],
    }, best_sample_score


def build_feedback_sample_signature(card):
    grayscale = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale, 50, 150)
    name_main = cv2.cvtColor(crop_relative_region(card, *QWEN_NAME_MAIN_REGION), cv2.COLOR_BGR2GRAY)
    name_alt = cv2.cvtColor(crop_relative_region(card, *QWEN_NAME_ALT_REGION), cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(extract_frame_signature(card), cv2.COLOR_BGR2GRAY)

    return {
        'full': cv2.resize(grayscale, (128, 192), interpolation=cv2.INTER_AREA),
        'edges': cv2.resize(edges, (128, 192), interpolation=cv2.INTER_NEAREST),
        'name_main': cv2.resize(name_main, (196, 72), interpolation=cv2.INTER_AREA),
        'name_alt': cv2.resize(name_alt, (196, 72), interpolation=cv2.INTER_AREA),
        'frame': cv2.resize(frame, (128, 192), interpolation=cv2.INTER_AREA),
    }


@lru_cache(maxsize=512)
def load_feedback_sample_signature(sample_path):
    if not sample_path:
        return None

    image_path = OCR_FEEDBACK_PATH.parent / str(sample_path)
    if not image_path.exists():
        return None

    sample_image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if sample_image is None or not sample_image.size:
        return None

    return build_feedback_sample_signature(sample_image)


def score_feedback_sample_signature(card_signature, sample_signature):
    if not card_signature or not sample_signature:
        return 0.0

    full_score = sanitize_template_score(cv2.matchTemplate(card_signature['full'], sample_signature['full'], cv2.TM_CCOEFF_NORMED))
    edge_score = sanitize_template_score(cv2.matchTemplate(card_signature['edges'], sample_signature['edges'], cv2.TM_CCORR_NORMED))
    name_main_score = sanitize_template_score(cv2.matchTemplate(card_signature['name_main'], sample_signature['name_main'], cv2.TM_CCOEFF_NORMED))
    name_alt_score = sanitize_template_score(cv2.matchTemplate(card_signature['name_alt'], sample_signature['name_alt'], cv2.TM_CCOEFF_NORMED))
    frame_score = sanitize_template_score(cv2.matchTemplate(card_signature['frame'], sample_signature['frame'], cv2.TM_CCOEFF_NORMED))
    return (
        (full_score * 0.28)
        + (edge_score * 0.18)
        + (name_main_score * 0.26)
        + (name_alt_score * 0.18)
        + (frame_score * 0.10)
    )


def get_top_manifest_entry_candidates(name_candidates, manifest, limit=4, support_text=''):
    ranked_entries = []

    for entry in manifest:
        best_candidate_score = 0.0
        for candidate in name_candidates:
            score = score_manifest_candidate(candidate, entry, support_text=support_text)
            best_candidate_score = max(best_candidate_score, score)
        ranked_entries.append({**entry, 'candidateScore': best_candidate_score})

    ranked_entries.sort(key=lambda item: item['candidateScore'], reverse=True)
    deduped = []
    seen = set()
    for entry in ranked_entries:
        entry_key = entry.get('entryKey')
        if not entry_key or entry_key in seen:
            continue
        seen.add(entry_key)
        deduped.append(entry)
        if len(deduped) >= limit:
            break

    return deduped


def is_ambiguous_name_candidate_set(name_candidates):
    if not name_candidates:
        return True

    for candidate in name_candidates:
        lowered = str(candidate).lower()
        if 'lcb sinner' in lowered:
            return True

    longest_candidate = max((len(tokenize_name(candidate)) for candidate in name_candidates), default=0)
    return longest_candidate <= 3


def match_manifest_sinner_label(sinner_key, labels):
    if not sinner_key or not labels:
        return False

    normalized_key = normalize_manifest_sinner_key(sinner_key)
    for label in labels:
        if normalized_key in SINNER_ICON_ALIASES.get(label, (label,)):
            return True

    return False


def normalize_manifest_sinner_key(sinner_key):
    return re.sub(r'(IDs|EGOs)$', '', str(sinner_key or ''))


def rank_identity_icon_matches(card):
    top_band_variants = extract_identity_icon_regions(card)
    if not top_band_variants:
        return []

    scores = {}

    for template in load_identity_icon_templates():
        best_score = 0.0
        for crop in top_band_variants:
            best_score = max(best_score, score_identity_icon_template(crop, template))

        if best_score > 0.0:
            scores[template['label']] = max(scores.get(template['label'], 0.0), best_score)

    return [
        {'label': label, 'score': score}
        for label, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
    ]


def extract_identity_icon_regions(card):
    regions = []
    height, width = card.shape[:2]

    for left, top, right, bottom in IDENTITY_ICON_REGIONS:
        x1 = max(0, int(width * left))
        y1 = max(0, int(height * top))
        x2 = min(width, int(width * right))
        y2 = min(height, int(height * bottom))
        if x2 <= x1 or y2 <= y1:
            continue

        crop = card[y1:y2, x1:x2]
        if crop.size:
            regions.append(crop)

    return regions


def score_identity_icon_template(crop, template):
    crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _threshold, crop_dark = cv2.threshold(crop_gray, 156, 255, cv2.THRESH_BINARY_INV)
    crop_dark = cv2.morphologyEx(crop_dark, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    crop_edges = cv2.Canny(crop_gray, 70, 180)
    crop_height, crop_width = crop_gray.shape[:2]
    best_score = 0.0

    for scale_ratio in IDENTITY_ICON_SCALE_RATIOS:
        target_height = int(crop_height * scale_ratio)
        if target_height < 12:
            continue

        scale = target_height / float(template['height'])
        target_width = int(template['width'] * scale)
        if target_width < 12 or target_width >= crop_width or target_height >= crop_height:
            continue

        interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
        resized_dark = cv2.resize(template['dark'], (target_width, target_height), interpolation=interpolation)
        resized_edges = cv2.resize(template['edges'], (target_width, target_height), interpolation=cv2.INTER_NEAREST)
        resized_mask = cv2.resize(template['mask'], (target_width, target_height), interpolation=cv2.INTER_NEAREST)

        if np.count_nonzero(resized_mask) < 24:
            continue

        dark_score = sanitize_template_score(cv2.matchTemplate(crop_dark, resized_dark, cv2.TM_CCORR_NORMED, mask=resized_mask))
        edge_score = sanitize_template_score(cv2.matchTemplate(crop_edges, resized_edges, cv2.TM_CCORR_NORMED, mask=resized_mask))
        best_score = max(best_score, (dark_score * 0.65) + (edge_score * 0.35))

    return best_score


def sanitize_template_score(result):
    if result is None or not getattr(result, 'size', 0):
        return 0.0

    finite = result[np.isfinite(result)]
    if not finite.size:
        return 0.0

    return float(np.clip(finite.max(), 0.0, 1.0))


@lru_cache(maxsize=1)
def load_identity_icon_templates():
    templates = []

    if not IDENTITY_ICON_TEMPLATES_DIR.exists():
        return tuple()

    for template_path in sorted(IDENTITY_ICON_TEMPLATES_DIR.iterdir()):
        if template_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        template = cv2.imread(str(template_path), cv2.IMREAD_UNCHANGED)
        if template is None or template.ndim != 3:
            continue

        if template.shape[2] == 4:
            alpha = template[:, :, 3]
            color = template[:, :, :3]
        else:
            color = template[:, :, :3]
            alpha = np.where(cv2.cvtColor(color, cv2.COLOR_BGR2GRAY) < 250, 255, 0).astype(np.uint8)

        gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        _threshold, dark = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
        dark = cv2.bitwise_and(dark, dark, mask=alpha)
        edges = cv2.Canny(gray, 70, 180)
        edges = cv2.bitwise_and(edges, edges, mask=alpha)

        if not np.count_nonzero(alpha):
            continue

        templates.append(
            {
                'label': template_path.stem,
                'width': gray.shape[1],
                'height': gray.shape[0],
                'mask': alpha,
                'dark': dark,
                'edges': edges,
            }
        )

    return tuple(templates)


def collect_card_ocr_candidates(card, normalized_regions, whitelist='', ocr_result=None):
    candidates = []
    seen = set()
    if ocr_result is None:
        ocr_result = extract_card_ocr_result(card)

    raw_candidates = []
    if ocr_result.get('level'):
        raw_candidates.append(ocr_result['level'])
        raw_candidates.append(f"Lv {ocr_result['level']}")

    raw_candidates.extend(
        [
            ocr_result.get('name', ''),
            ocr_result.get('tagged_name', ''),
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
    analysis_image = build_qwen_card_ocr_image(card)
    image_bytes = encode_png_bytes(analysis_image)
    return run_qwen_card_ocr(image_bytes)


def build_qwen_card_ocr_image(card):
    name_main = crop_relative_region(card, *QWEN_NAME_MAIN_REGION)
    name_alt = enhance_identity_text_region(crop_relative_region(card, *QWEN_NAME_FOCUS_REGION))
    panels = [
        build_qwen_labeled_panel('CARD', card),
        build_qwen_labeled_panel('NAME MAIN', name_main),
        build_qwen_labeled_panel('NAME ALT', name_alt),
        build_qwen_labeled_panel('SINNER ICON', crop_relative_region(card, *QWEN_SINNER_ICON_REGION)),
        build_qwen_labeled_panel('LEVEL', crop_relative_region(card, *QWEN_LEVEL_REGION)),
    ]

    return stack_qwen_panels(panels)


def build_qwen_card_name_choice_image(card, candidates):
    name_main = crop_relative_region(card, *QWEN_NAME_MAIN_REGION)
    name_alt = enhance_identity_text_region(crop_relative_region(card, *QWEN_NAME_FOCUS_REGION))
    panels = [
        build_qwen_labeled_panel('CARD', card),
        build_qwen_labeled_panel('NAME MAIN', name_main),
        build_qwen_labeled_panel('NAME ALT', name_alt),
        build_qwen_labeled_panel('SINNER ICON', crop_relative_region(card, *QWEN_SINNER_ICON_REGION)),
        build_qwen_labeled_panel('LEVEL', crop_relative_region(card, *QWEN_LEVEL_REGION)),
    ]

    for index, entry in enumerate(candidates, start=1):
        panels.append(build_qwen_labeled_panel(f'C{index}', build_qwen_text_block(entry['entryKey'])))

    return stack_qwen_panels(panels)


def extract_card_uptie_result(card, matched_entry=None, detected_label=''):
    rarity = normalize_rarity((matched_entry or {}).get('rarity')) or infer_known_label_rarity(detected_label)
    candidates = get_top_frame_template_candidates(card, rarity=rarity, limit=2)

    if not candidates:
        return ''

    if len(candidates) == 1:
        return str(candidates[0]['uptie_level'])

    if candidates[0]['uptie_level'] == candidates[1]['uptie_level']:
        return str(candidates[0]['uptie_level'])

    analysis_image = build_qwen_uptie_choice_image(card, matched_entry, detected_label)
    image_bytes = encode_png_bytes(analysis_image)
    choice = run_qwen_card_uptie(image_bytes)
    if choice == 'C1':
        return str(candidates[0]['uptie_level'])
    if choice == 'C2':
        return str(candidates[1]['uptie_level'])

    return ''


def build_qwen_card_uptie_image(card):
    panels = [
        build_qwen_labeled_panel('TOP RIGHT FRAME', crop_relative_region(card, *QWEN_UPTIE_TOP_RIGHT_REGION)),
        build_qwen_labeled_panel('BOTTOM LEFT FRAME', crop_relative_region(card, *QWEN_UPTIE_BOTTOM_LEFT_REGION)),
    ]

    return stack_qwen_panels(panels)


def build_qwen_uptie_choice_image(card, matched_entry=None, detected_label=''):
    rarity = normalize_rarity((matched_entry or {}).get('rarity')) or infer_known_label_rarity(detected_label)
    candidates = get_top_frame_template_candidates(card, rarity=rarity, limit=2)
    panels = [
        build_qwen_labeled_panel('CARD TOP RIGHT', crop_relative_region(card, *QWEN_UPTIE_TOP_RIGHT_REGION)),
        build_qwen_labeled_panel('CARD BOTTOM LEFT', crop_relative_region(card, *QWEN_UPTIE_BOTTOM_LEFT_REGION)),
    ]

    for index, candidate in enumerate(candidates, start=1):
        template_signature = candidate['signature_color']
        panels.append(
            build_qwen_labeled_panel(
                f'C{index} U{candidate["uptie_level"]} TR {candidate["score"]:.3f}',
                crop_relative_region(template_signature, *QWEN_UPTIE_TOP_RIGHT_REGION),
            )
        )
        panels.append(
            build_qwen_labeled_panel(
                f'C{index} U{candidate["uptie_level"]} BL {candidate["score"]:.3f}',
                crop_relative_region(template_signature, *QWEN_UPTIE_BOTTOM_LEFT_REGION),
            )
        )

    return stack_qwen_panels(panels)


def stack_qwen_panels(panels):
    if not panels:
        return np.full((QWEN_PANEL_LABEL_HEIGHT, QWEN_PANEL_WIDTH, 3), 255, dtype=np.uint8)

    canvas_width = max(panel.shape[1] for panel in panels)
    canvas_height = sum(panel.shape[0] for panel in panels) + (QWEN_PANEL_GAP * (len(panels) - 1))
    canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)

    offset_y = 0
    for panel in panels:
        panel_height, panel_width = panel.shape[:2]
        canvas[offset_y:offset_y + panel_height, 0:panel_width] = panel
        offset_y += panel_height + QWEN_PANEL_GAP

    return canvas


def crop_relative_region(card, left, top, right, bottom):
    height, width = card.shape[:2]
    x1 = max(0, min(width - 1, int(width * left)))
    y1 = max(0, min(height - 1, int(height * top)))
    x2 = max(x1 + 1, min(width, int(width * right)))
    y2 = max(y1 + 1, min(height, int(height * bottom)))
    return card[y1:y2, x1:x2]


def build_qwen_labeled_panel(label, image):
    if image is None or not image.size:
        image = np.full((32, QWEN_PANEL_WIDTH, 3), 255, dtype=np.uint8)

    panel_height, panel_width = image.shape[:2]
    scale = QWEN_PANEL_WIDTH / float(panel_width)
    target_height = max(32, int(round(panel_height * scale)))
    resized = cv2.resize(image, (QWEN_PANEL_WIDTH, target_height), interpolation=cv2.INTER_CUBIC)

    panel = np.full((target_height + QWEN_PANEL_LABEL_HEIGHT, QWEN_PANEL_WIDTH, 3), 255, dtype=np.uint8)
    panel[:QWEN_PANEL_LABEL_HEIGHT] = 235
    panel[QWEN_PANEL_LABEL_HEIGHT:] = resized
    cv2.putText(panel, label, (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (32, 32, 32), 2, cv2.LINE_AA)
    return panel


def build_qwen_text_block(text):
    normalized = normalize_ocr_text(text or '') or ' '
    canvas = np.full((120, QWEN_PANEL_WIDTH, 3), 255, dtype=np.uint8)
    words = normalized.split()
    lines = []
    current_line = ''

    for word in words:
        proposed = f'{current_line} {word}'.strip()
        text_width = cv2.getTextSize(proposed, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0][0]
        if current_line and text_width > (QWEN_PANEL_WIDTH - 24):
            lines.append(current_line)
            current_line = word
        else:
            current_line = proposed

    if current_line:
        lines.append(current_line)

    for index, line in enumerate(lines[:4]):
        y = 28 + (index * 24)
        cv2.putText(canvas, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (24, 24, 24), 2, cv2.LINE_AA)

    return canvas


def enhance_identity_text_region(image):
    if image is None or not image.size:
        return image

    scale = 2.0 if max(image.shape[:2]) < 220 else 1.5
    resized = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(grayscale, None, 0, 255, cv2.NORM_MINMAX)
    blurred = cv2.GaussianBlur(normalized, (0, 0), 1.1)
    sharpened = cv2.addWeighted(normalized, 1.45, blurred, -0.45, 0)
    thresholded = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7,
    )
    cleaned = cv2.medianBlur(thresholded, 3)
    return cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)


def encode_png_bytes(image):
    success, encoded = cv2.imencode('.png', image)
    if not success:
        raise ValueError('Failed to encode image payload for OCR.')

    return encoded.tobytes()


@lru_cache(maxsize=96)
def run_qwen_card_ocr(image_bytes):
    started_at = time.perf_counter()
    try:
        output_text = generate_qwen_response(
            image_bytes,
            QWEN_CARD_OCR_PROMPT,
            max_new_tokens=int(os.environ.get('QWEN_VL_OCR_MAX_NEW_TOKENS', str(DEFAULT_QWEN_OCR_MAX_NEW_TOKENS))),
        )
    except Exception as exc:
        raise RuntimeError(f'Qwen3-VL OCR request failed: {exc}') from exc

    log_recognition_timing('qwen_ocr', seconds=f'{time.perf_counter() - started_at:.3f}', bytes=len(image_bytes))

    return parse_qwen_card_ocr_output(output_text)


@lru_cache(maxsize=96)
def run_qwen_card_uptie(image_bytes):
    started_at = time.perf_counter()
    try:
        output_text = generate_qwen_response(
            image_bytes,
            QWEN_CARD_UPTIE_PROMPT,
            max_new_tokens=int(os.environ.get('QWEN_VL_CHOICE_MAX_NEW_TOKENS', str(DEFAULT_QWEN_CHOICE_MAX_NEW_TOKENS))),
        )
    except Exception as exc:
        raise RuntimeError(f'Qwen3-VL uptie request failed: {exc}') from exc

    log_recognition_timing('qwen_uptie', seconds=f'{time.perf_counter() - started_at:.3f}', bytes=len(image_bytes))

    return parse_qwen_card_uptie_output(output_text)


@lru_cache(maxsize=96)
def run_qwen_card_name_choice(image_bytes):
    started_at = time.perf_counter()
    try:
        output_text = generate_qwen_response(
            image_bytes,
            QWEN_CARD_NAME_CHOICE_PROMPT,
            max_new_tokens=int(os.environ.get('QWEN_VL_CHOICE_MAX_NEW_TOKENS', str(DEFAULT_QWEN_CHOICE_MAX_NEW_TOKENS))),
        )
    except Exception as exc:
        raise RuntimeError(f'Qwen3-VL name-choice request failed: {exc}') from exc

    log_recognition_timing('qwen_name_choice', seconds=f'{time.perf_counter() - started_at:.3f}', bytes=len(image_bytes))

    return parse_qwen_card_name_choice_output(output_text)


def generate_qwen_response(image_bytes, prompt_text, max_new_tokens=DEFAULT_QWEN_OCR_MAX_NEW_TOKENS):
    model, processor = get_qwen_vl_components()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'image'},
                {'type': 'text', 'text': prompt_text},
            ],
        }
    ]
    prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[prompt], images=[image], return_tensors='pt')
    device = get_qwen_vl_device(model)
    inputs = {key: value.to(device) if hasattr(value, 'to') else value for key, value in inputs.items()}
    generation_config = copy.deepcopy(model.generation_config)
    generation_config.do_sample = False
    generation_config.temperature = None
    generation_config.top_p = None
    generation_config.top_k = None

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            generation_config=generation_config,
            max_new_tokens=int(max_new_tokens),
            do_sample=False,
        )

    trimmed_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs['input_ids'], generated_ids)]
    return processor.batch_decode(trimmed_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]


@lru_cache(maxsize=1)
def get_qwen_vl_components():
    model_name = os.environ.get('QWEN_VL_MODEL', DEFAULT_QWEN_VL_MODEL)
    model_kwargs = {
        'dtype': resolve_qwen_torch_dtype(),
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
    tagged_fields = extract_tagged_fields(output_text)

    name = normalize_ocr_text(str((payload or {}).get('name', '') or tagged_fields.get('name', '')))
    sinner = normalize_ocr_text(str((payload or {}).get('sinner', '') or tagged_fields.get('sinner', '')))
    level = normalize_ocr_text(str((payload or {}).get('level', '') or tagged_fields.get('level', '')))
    text = normalize_ocr_text(str((payload or {}).get('text', '') or tagged_fields.get('text', '')))

    if not text:
        text = normalized_output

    name = cleanup_identity_name(name)
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
        'sinner': sinner,
        'tagged_name': tagged_fields.get('name', ''),
        'level': level,
        'text': text,
        'raw_output': normalized_output,
    }


def parse_qwen_card_uptie_output(output_text):
    match = QWEN_UPTIE_CHOICE_REGEX.search(str(output_text)) or re.search(r'\b(C[12])\b', str(output_text), flags=re.IGNORECASE)
    return match.group(1).upper() if match else ''


def parse_qwen_card_name_choice_output(output_text):
    match = QWEN_NAME_CHOICE_REGEX.search(str(output_text)) or re.search(r'\b(C[1-4])\b', str(output_text), flags=re.IGNORECASE)
    return match.group(1).upper() if match else ''


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


def extract_tagged_fields(text):
    fields = {}

    for match in QWEN_TAGGED_FIELD_REGEX.finditer(str(text)):
        key = match.group(1).lower()
        value = normalize_ocr_text(match.group(2))
        if value:
            fields[key] = value

    return fields


def cleanup_identity_name(text):
    cleaned = normalize_ocr_text(text)
    cleaned = re.sub(r'^(?:name|text)\s*[:=-]\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bsinner\b.*$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b(?:new|lv|level)\b.*$', '', cleaned, flags=re.IGNORECASE)
    cleaned = collapse_repeated_token_sequence(cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(" -.:')(")
    return cleaned


def score_identity_text(text):
    letters = len(re.findall(r'[A-Za-z]', text))
    digits = len(re.findall(r'\d', text))
    punctuation_noise = len(re.findall(r"[^A-Za-z0-9\s\-\.'/\":]", text))
    return (letters * 2.0) + min(digits, 3) - (punctuation_noise * 1.5)


def normalize_ocr_text(text):
    normalized = str(text or '')
    for source, target in (
        ('\r', ' '),
        ('\n', ' '),
        ('|', 'I'),
        ('—', '-'),
        ('–', '-'),
        ('’', "'"),
        ('‘', "'"),
        ('“', '"'),
        ('”', '"'),
    ):
        normalized = normalized.replace(source, target)

    return collapse_repeated_token_sequence(' '.join(normalized.split()))


def collapse_repeated_token_sequence(text, max_window=4):
    tokens = str(text or '').split()
    if len(tokens) < 2:
        return ' '.join(tokens)

    normalized_tokens = [sanitize_name(token) for token in tokens]
    changed = True

    while changed and len(tokens) >= 2:
        changed = False
        max_candidate_window = min(max_window, len(tokens) // 2)
        for window in range(max_candidate_window, 0, -1):
            if normalized_tokens[-window:] and normalized_tokens[-window:] == normalized_tokens[-(window * 2):-window]:
                tokens = tokens[:-window]
                normalized_tokens = normalized_tokens[:-window]
                changed = True
                break

    deduped_tokens = []
    for token, normalized_token in zip(tokens, normalized_tokens):
        if deduped_tokens and normalized_token == sanitize_name(deduped_tokens[-1]):
            continue
        deduped_tokens.append(token)

    return ' '.join(deduped_tokens)


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


def build_manifest_token_weights(manifest):
    document_frequency = {}

    for entry in manifest:
        entry_tokens = set(entry.get('name_tokens') or ())
        for alias_tokens in entry.get('match_alias_tokens') or ():
            entry_tokens.update(alias_tokens)

        for token in entry_tokens:
            document_frequency[token] = document_frequency.get(token, 0) + 1

    total_entries = max(len(manifest), 1)
    return {
        token: 1.0 + max(0.0, 1.8 - (frequency / total_entries * 3.0))
        for token, frequency in document_frequency.items()
    }


def weighted_overlap_score(left_tokens, right_tokens, token_weights):
    left_chunks = set(left_tokens)
    right_chunks = set(right_tokens)
    if not left_chunks or not right_chunks:
        return 0.0

    union_tokens = left_chunks | right_chunks
    denominator = sum(token_weights.get(token, 1.0) for token in union_tokens)
    if denominator <= 0:
        return 0.0

    numerator = sum(token_weights.get(token, 1.0) for token in (left_chunks & right_chunks))
    return numerator / denominator


def distinctive_token_score(input_tokens, entry_tokens, token_weights):
    entry_distinctive = [
        token for token in set(entry_tokens)
        if len(token) > 2 and token not in MANIFEST_TOKEN_STOPWORDS and token_weights.get(token, 1.0) >= 1.15
    ]
    if not entry_distinctive:
        return 0.0

    input_token_set = set(input_tokens)
    matched_weight = sum(token_weights.get(token, 1.0) for token in entry_distinctive if token in input_token_set)
    total_weight = sum(token_weights.get(token, 1.0) for token in entry_distinctive)
    if total_weight <= 0:
        return 0.0

    return matched_weight / total_weight


def ordered_distinctive_tokens(tokens, token_weights):
    ordered = []

    for token in tokens:
        if not token:
            continue
        if token in MANIFEST_TOKEN_STOPWORDS:
            continue
        if len(token) <= 1 and not token.isdigit():
            continue
        if not token.isdigit() and token_weights.get(token, 1.0) < 1.05:
            continue
        if ordered and ordered[-1] == token:
            continue
        ordered.append(token)

    return tuple(ordered)


def leading_distinctive_token_adjustment(input_tokens, entry_tokens, token_weights):
    input_distinctive = ordered_distinctive_tokens(input_tokens, token_weights)
    entry_distinctive = ordered_distinctive_tokens(entry_tokens, token_weights)

    if not input_distinctive or not entry_distinctive:
        return 0.0

    if input_distinctive[0] == entry_distinctive[0]:
        prefix_matches = 1
        for left_token, right_token in zip(input_distinctive[1:], entry_distinctive[1:]):
            if left_token != right_token:
                break
            prefix_matches += 1

        return min(0.18, 0.1 + ((prefix_matches - 1) * 0.04))

    if input_distinctive[0] in entry_distinctive[:2] or entry_distinctive[0] in input_distinctive[:2]:
        return 0.03

    return -0.12


def score_manifest_text_variant(raw_name, candidate_name, entry_tokens, token_weights):
    normalized_input = sanitize_name(raw_name)
    normalized_candidate = sanitize_name(candidate_name)
    if not normalized_input or not normalized_candidate:
        return 0.0

    input_tokens = tokenize_name(raw_name)
    ratio = difflib.SequenceMatcher(None, normalized_input, normalized_candidate).ratio()
    partial = partial_ratio(normalized_input, normalized_candidate)
    token_bonus = weighted_overlap_score(input_tokens, entry_tokens, token_weights)
    distinctive_bonus = distinctive_token_score(input_tokens, entry_tokens, token_weights)
    containment_bonus = 1.0 if normalized_input in normalized_candidate or normalized_candidate in normalized_input else 0.0
    leading_adjustment = leading_distinctive_token_adjustment(input_tokens, entry_tokens, token_weights)
    score = (
        (max(ratio, partial) * 0.5)
        + (token_bonus * 0.2)
        + (distinctive_bonus * 0.18)
        + (containment_bonus * 0.08)
        + leading_adjustment
    )
    return float(np.clip(score, 0.0, 1.0))


def score_feedback_text_profiles(raw_name, support_text, text_profiles, token_weights):
    if not text_profiles:
        return 0.0

    candidate_texts = []
    for candidate_text in (cleanup_identity_name(raw_name), cleanup_identity_name(support_text)):
        if candidate_text and candidate_text not in candidate_texts:
            candidate_texts.append(candidate_text)

    if not candidate_texts:
        return 0.0

    best_score = 0.0
    for profile in text_profiles:
        for profile_text in (
            profile.get('observed_name', ''),
            profile.get('raw_ocr_name', ''),
            profile.get('ocr_support_text', ''),
        ):
            if not profile_text:
                continue

            profile_tokens = tokenize_name(profile_text)
            for candidate_text in candidate_texts:
                profile_score = score_manifest_text_variant(candidate_text, profile_text, profile_tokens, token_weights)
                if sanitize_name(candidate_text) == sanitize_name(profile_text):
                    profile_score = min(1.0, profile_score + ALIAS_MATCH_EXACT_BONUS)
                best_score = max(best_score, profile_score)

    return best_score


def score_manifest_candidate(raw_name, entry, token_weights=None, support_text=''):
    token_weights = token_weights or {}
    best_score = score_manifest_text_variant(raw_name, entry.get('entryKey', ''), entry.get('name_tokens') or (), token_weights)
    best_support_score = 0.0

    for alias, alias_tokens in zip(entry.get('match_aliases') or (), entry.get('match_alias_tokens') or ()):
        alias_score = score_manifest_text_variant(raw_name, alias, alias_tokens, token_weights)
        if sanitize_name(raw_name) == sanitize_name(alias):
            alias_score += ALIAS_MATCH_EXACT_BONUS
        best_score = max(best_score, alias_score)

        if support_text:
            best_support_score = max(best_support_score, score_manifest_text_variant(support_text, alias, alias_tokens, token_weights))

    if support_text:
        best_support_score = max(
            best_support_score,
            score_manifest_text_variant(support_text, entry.get('entryKey', ''), entry.get('name_tokens') or (), token_weights),
        )
        best_score = max(best_score, (best_score * 0.82) + (best_support_score * 0.18))

    feedback_profile_score = score_feedback_text_profiles(
        raw_name,
        support_text,
        entry.get('feedback_text_profiles') or (),
        token_weights,
    )
    if feedback_profile_score:
        best_score = max(best_score, (best_score * 0.76) + (feedback_profile_score * 0.24))

    return min(best_score, 1.0)


def match_manifest_entry(raw_name, manifest, support_text=''):
    normalized_input = sanitize_name(raw_name)
    best_entry = None
    best_score = 0.0
    second_best_score = 0.0

    if not normalized_input:
        return None, 0.0

    token_weights = build_manifest_token_weights(manifest)

    for entry in manifest:
        if not entry.get('normalized_name'):
            continue

        score = score_manifest_candidate(raw_name, entry, token_weights=token_weights, support_text=support_text)

        if score > best_score:
            second_best_score = best_score
            best_score = score
            best_entry = entry
        elif score > second_best_score:
            second_best_score = score

    if best_score < 0.4:
        return None, best_score

    if best_score < 0.8 and (best_score - second_best_score) < AMBIGUOUS_MATCH_SCORE_MARGIN:
        return None, best_score

    return {
        'sinnerKey': best_entry['sinnerKey'],
        'category': best_entry['category'],
        'entryKey': best_entry['entryKey'],
        'rarity': normalize_rarity(best_entry.get('rarity')),
        'hasLevel': best_entry['hasLevel'],
    }, best_score


def build_ocr_support_text(ocr_result):
    support_chunks = []

    for key in ('tagged_name', 'text', 'raw_output'):
        value = cleanup_identity_name((ocr_result or {}).get(key, ''))
        if not value:
            continue
        if value not in support_chunks:
            support_chunks.append(value)

    return ' '.join(support_chunks[:2])


def build_feedback_export_records():
    feedback_store = load_ocr_feedback_store()
    records = []

    for feedback_key, feedback_entry in sorted(feedback_store.items()):
        for example in feedback_entry.get('examples', []):
            input_payload = example.get('input', {})
            target_payload = example.get('target', {})
            records.append(
                {
                    'feedback_key': feedback_key,
                    'image_path': example.get('image_path', ''),
                    'input': input_payload,
                    'target': target_payload,
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Read one Limbus Company identity card crop and map it to the canonical roster entry.',
                        },
                        {
                            'role': 'user',
                            'content': json.dumps(input_payload, ensure_ascii=True, sort_keys=True),
                        },
                        {
                            'role': 'assistant',
                            'content': json.dumps(target_payload, ensure_ascii=True, sort_keys=True),
                        },
                    ],
                }
            )

    return records


def export_ocr_feedback_dataset(output_format='json'):
    records = build_feedback_export_records()
    if str(output_format or '').lower() == 'jsonl':
        return '\n'.join(json.dumps(record, ensure_ascii=True) for record in records)

    return {
        'count': len(records),
        'records': records,
    }


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


def infer_uptie(card, matched_entry=None, detected_label=''):
    rarity = normalize_rarity((matched_entry or {}).get('rarity')) or infer_known_label_rarity(detected_label)
    template_level, template_confidence = match_frame_templates(card, rarity=rarity)
    if template_level is not None:
        return template_level, template_confidence

    qwen_uptie = extract_card_uptie_result(card, matched_entry, detected_label)
    if qwen_uptie in {'1', '2', '3', '4'}:
        return int(qwen_uptie), 0.56

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
    level_scores = collect_frame_level_scores(card, rarity=rarity)
    if not level_scores:
        return None, 0.0

    ranked_levels = sorted(level_scores.items(), key=lambda item: item[1], reverse=True)
    best_level, best_score = ranked_levels[0]
    second_score = ranked_levels[1][1] if len(ranked_levels) > 1 else 0.0
    threshold = FRAME_UPTIE_MATCH_THRESHOLD_WITH_RARITY if rarity else FRAME_UPTIE_MATCH_THRESHOLD

    if best_score < threshold:
        return None, 0.0

    if best_score - second_score < FRAME_UPTIE_MIN_MARGIN and best_level in (2, 3):
        higher_level_score = level_scores.get(best_level + 1, 0.0)
        if higher_level_score >= max(threshold - 0.03, best_score - 0.02):
            return best_level + 1, higher_level_score

    return best_level, best_score


def score_frame_templates(card, rarity=None):
    level_scores = collect_frame_level_scores(card, rarity=rarity)
    if not level_scores:
        return None, 0.0

    best_level, best_score = max(level_scores.items(), key=lambda item: item[1])
    return best_level, best_score


def collect_frame_level_scores(card, rarity=None):
    signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(signature, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    edges = cv2.Canny(grayscale, 50, 150)
    level_scores = {}

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
        level_scores[template['uptie_level']] = max(level_scores.get(template['uptie_level'], 0.0), score)

    return level_scores


def get_top_frame_template_candidates(card, rarity=None, limit=2):
    signature = extract_frame_signature(card)
    grayscale = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(signature, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    edges = cv2.Canny(grayscale, 50, 150)
    candidates = []

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
        candidates.append(
            {
                'uptie_level': template['uptie_level'],
                'template_name': template['template_name'],
                'rarity': template['rarity'],
                'score': score,
                'signature_color': template['signature_color'],
            }
        )

    candidates.sort(key=lambda item: item['score'], reverse=True)
    return candidates[:limit]


@lru_cache(maxsize=24)
def load_scaled_frame_templates(target_height, target_width):
    scaled_templates = []

    for template in load_frame_templates():
        scaled_templates.append(
            {
                'uptie_level': template['uptie_level'],
                'template_name': template['template_name'],
                'rarity': template['rarity'],
                'grayscale': cv2.resize(template['grayscale'], (target_width, target_height)),
                'edges': cv2.resize(template['edges'], (target_width, target_height), interpolation=cv2.INTER_NEAREST),
                'saturation': cv2.resize(template['saturation'], (target_width, target_height)),
                'value': cv2.resize(template['value'], (target_width, target_height)),
                'signature_color': cv2.resize(template['signature_color'], (target_width, target_height)),
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
                    'template_name': template_path.stem,
                    'rarity': parse_template_rarity(template_path),
                    'grayscale': grayscale,
                    'edges': edges,
                    'saturation': hsv[:, :, 1],
                    'value': hsv[:, :, 2],
                    'signature_color': signature,
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
    mask_frame_overlays(signature)
    return signature


def mask_frame_overlays(signature):
    height, width = signature.shape[:2]
    if height <= 0 or width <= 0:
        return

    # Remove rarity pips and round badge overlays that do not exist in frame templates.
    cv2.rectangle(signature, (0, 0), (int(width * 0.28), int(height * 0.16)), (0, 0, 0), thickness=-1)
    cv2.circle(signature, (int(width * 0.86), int(height * 0.08)), int(min(height, width) * 0.14), (0, 0, 0), thickness=-1)
    cv2.rectangle(signature, (int(width * 0.36), 0), (int(width * 0.64), int(height * 0.08)), (0, 0, 0), thickness=-1)


def infer_known_label_rarity(text):
    normalized_text = normalize_detected_label(str(text or ''), None, 0.0, [])
    return KNOWN_OCR_LABEL_RARITIES.get(normalized_text)


def build_card_debug_report(card, matched_entry=None, detected_label=''):
    ocr_result = extract_card_ocr_result(card)
    rarity = normalize_rarity((matched_entry or {}).get('rarity')) or infer_known_label_rarity(detected_label or ocr_result.get('name', ''))
    return {
        'ocr': ocr_result,
        'qwen_uptie': extract_card_uptie_result(card, matched_entry, detected_label or ocr_result.get('name', '')),
        'uptie_template_candidates': [
            {
                'uptie_level': candidate['uptie_level'],
                'template_name': candidate['template_name'],
                'rarity': candidate['rarity'],
                'score': round(candidate['score'], 4),
            }
            for candidate in get_top_frame_template_candidates(card, rarity=rarity, limit=2)
        ],
        'name_candidates': extract_name_candidates(card),
        'level': extract_level(card),
        'frame_scores_any': collect_frame_level_scores(card),
        'frame_scores_rarity': collect_frame_level_scores(card, rarity=rarity) if rarity else {},
        'inferred_uptie': infer_uptie(card, matched_entry, detected_label or ocr_result.get('name', '')),
        'rarity_hint': rarity,
    }


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