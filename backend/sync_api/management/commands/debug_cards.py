import json
from pathlib import Path

import cv2
from django.core.management.base import BaseCommand, CommandError

from sync_api import services


class Command(BaseCommand):
    help = 'Dump per-card OCR and frame-debug information for one or more screenshots.'

    def add_arguments(self, parser):
        parser.add_argument('images', nargs='+', help='Image paths to inspect.')
        parser.add_argument(
            '--output-dir',
            default='',
            help='Optional directory where cropped card PNGs and JSON reports will be written.',
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output_dir']).resolve() if options['output_dir'] else None
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

        for image_arg in options['images']:
            image_path = Path(image_arg).resolve()
            if not image_path.exists():
                raise CommandError(f'Image not found: {image_path}')

            image = services.decode_image(image_path.read_bytes())
            regions = services.extract_card_regions(image)
            self.stdout.write(f'Image: {image_path}')
            self.stdout.write(f'Cards detected: {len(regions)}')

            image_output_dir = None
            if output_dir:
                image_output_dir = output_dir / image_path.stem
                image_output_dir.mkdir(parents=True, exist_ok=True)

            reports = []
            for index, bounds in enumerate(regions, start=1):
                x, y, width, height = bounds
                card = image[y:y + height, x:x + width]
                debug_report = services.build_card_debug_report(card)
                report = {
                    'index': index,
                    'bounds': {'x': x, 'y': y, 'width': width, 'height': height},
                    **debug_report,
                }
                reports.append(report)

                self.stdout.write(f'  Card {index:02d}: bounds={bounds}')
                self.stdout.write(f"    OCR name={report['ocr'].get('name', '')!r} level={report['ocr'].get('level', '')!r}")
                self.stdout.write(f"    Name candidates={report['name_candidates']}")
                self.stdout.write(f"    Frame any={json.dumps(report['frame_scores_any'], sort_keys=True)}")
                self.stdout.write(f"    Frame rarity={json.dumps(report['frame_scores_rarity'], sort_keys=True)}")
                self.stdout.write(f"    Inferred uptie={report['inferred_uptie']}")

                if image_output_dir:
                    crop_path = image_output_dir / f'card_{index:02d}.png'
                    uptie_choice_path = image_output_dir / f'card_{index:02d}_uptie_choice.png'
                    report_path = image_output_dir / f'card_{index:02d}.json'
                    cv2.imwrite(str(crop_path), card)
                    cv2.imwrite(str(uptie_choice_path), services.build_qwen_uptie_choice_image(card))
                    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

            if image_output_dir:
                summary_path = image_output_dir / 'summary.json'
                summary_path.write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding='utf-8')
                self.stdout.write(f'  Wrote debug output to {image_output_dir}')