import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import merge_updates_into_progress, recognize_screenshots_payload


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

    recognition = recognize_screenshots_payload(images, roster_manifest)
    merged_progress = merge_updates_into_progress(current_progress, recognition['updates'])

    return JsonResponse(
        {
            'processed_screenshots': recognition['processed_screenshots'],
            'updates': recognition['updates'],
            'cards': recognition['cards'],
            'merged_progress': merged_progress,
        }
    )