import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import (
    export_ocr_feedback_dataset,
    merge_updates_into_progress,
    recognize_screenshots_payload,
    store_recognition_feedback,
)


def healthcheck(_request):
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def recognize_screenshots(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)

    images = request.FILES.getlist('images')
    if not images:
        return JsonResponse({'detail': 'At least one image is required.'}, status=400)

    try:
        roster_manifest = json.loads(request.POST.get('roster_manifest', '[]'))
        current_progress = json.loads(request.POST.get('current_progress', '{}'))
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON payload.'}, status=400)

    try:
        recognition = recognize_screenshots_payload(images, roster_manifest)
    except RuntimeError as exc:
        return JsonResponse({'detail': str(exc)}, status=503)

    merged_progress = merge_updates_into_progress(current_progress, recognition['updates'])

    return JsonResponse(
        {
            'processed_screenshots': recognition['processed_screenshots'],
            'updates': recognition['updates'],
            'cards': recognition['cards'],
            'merged_progress': merged_progress,
        }
    )


@csrf_exempt
def record_recognition_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON payload.'}, status=400)

    feedback_items = payload.get('feedback') or []
    if not isinstance(feedback_items, list):
        return JsonResponse({'detail': 'Feedback payload must be a list.'}, status=400)

    persisted = store_recognition_feedback(feedback_items)
    return JsonResponse({'saved_feedback': persisted})


def export_recognition_feedback(request):
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)

    output_format = request.GET.get('format', 'json')
    payload = export_ocr_feedback_dataset(output_format=output_format)
    if str(output_format).lower() == 'jsonl':
        return HttpResponse(payload, content_type='application/x-ndjson; charset=utf-8')

    return JsonResponse(payload)