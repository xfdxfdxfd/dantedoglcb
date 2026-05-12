import json

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token as google_id_token
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UserProgress


AUTH_TOKEN_SALT = 'sync_api.auth'
AUTH_TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 30


def parse_json_body(request):
    try:
        return json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return None


def build_json_error(message, status):
    return JsonResponse({'detail': message}, status=status)


def create_auth_token(user):
    return signing.dumps({'user_id': user.pk}, salt=AUTH_TOKEN_SALT)


def get_bearer_token(request):
    header = request.headers.get('Authorization', '')
    token_type, _, token_value = header.partition(' ')

    if token_type.lower() != 'bearer' or not token_value:
        return None

    return token_value.strip()


def get_authenticated_user(request):
    token = get_bearer_token(request)

    if not token:
        return None

    try:
        payload = signing.loads(token, salt=AUTH_TOKEN_SALT, max_age=AUTH_TOKEN_MAX_AGE_SECONDS)
    except signing.BadSignature:
        return None
    except signing.SignatureExpired:
        return None

    user_id = payload.get('user_id')

    if not user_id:
        return None

    return get_user_model().objects.filter(pk=user_id).first()


def get_progress_payload(user):
    progress_record, _ = UserProgress.objects.get_or_create(user=user)
    return {
        'progress': progress_record.progress,
        'updated_at': progress_record.updated_at.isoformat(),
    }


def build_auth_payload(user):
    progress_payload = get_progress_payload(user)
    return {
        'token': create_auth_token(user),
        'user': {
            'email': user.email,
        },
        **progress_payload,
    }


def require_authenticated_user(request):
    user = get_authenticated_user(request)

    if user:
        return user, None

    return None, build_json_error('Authentication required.', 401)


def get_google_client_ids():
    return set(getattr(settings, 'GOOGLE_OAUTH_CLIENT_IDS', []) or [])


def verify_google_credential(credential):
    allowed_client_ids = get_google_client_ids()

    if not allowed_client_ids:
        raise ValueError('Google sign-in is not configured.')

    token_payload = google_id_token.verify_oauth2_token(credential, GoogleRequest(), audience=None)
    audience = str(token_payload.get('aud') or '')

    if audience not in allowed_client_ids:
        raise ValueError('Google client is not allowed.')

    if not token_payload.get('email_verified'):
        raise ValueError('Google account email is not verified.')

    return token_payload


def get_or_create_google_user(token_payload):
    email = str(token_payload.get('email') or '').strip().lower()

    if not email:
        raise ValueError('Google account did not provide an email address.')

    user_model = get_user_model()
    user = user_model.objects.filter(email=email).first()

    if user is None:
        user = user_model.objects.create_user(username=email, email=email)
        user.set_unusable_password()
        user.save(update_fields=['password'])

    UserProgress.objects.get_or_create(user=user)
    return user


def healthcheck(_request):
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def sign_up(request):
    if request.method != 'POST':
        return build_json_error('Method not allowed.', 405)

    payload = parse_json_body(request)
    if payload is None:
        return build_json_error('Invalid JSON payload.', 400)

    email = str(payload.get('email') or '').strip().lower()
    password = str(payload.get('password') or '')

    if not email or not password:
        return build_json_error('Email and password are required.', 400)

    try:
        validate_email(email)
    except ValidationError:
        return build_json_error('A valid email address is required.', 400)

    if len(password) < 8:
        return build_json_error('Password must be at least 8 characters long.', 400)

    user_model = get_user_model()
    if user_model.objects.filter(username=email).exists():
        return build_json_error('An account with that email already exists.', 409)

    user = user_model.objects.create_user(username=email, email=email, password=password)
    UserProgress.objects.get_or_create(user=user)
    return JsonResponse(build_auth_payload(user), status=201)


@csrf_exempt
def log_in(request):
    if request.method != 'POST':
        return build_json_error('Method not allowed.', 405)

    payload = parse_json_body(request)
    if payload is None:
        return build_json_error('Invalid JSON payload.', 400)

    email = str(payload.get('email') or '').strip().lower()
    password = str(payload.get('password') or '')

    if not email or not password:
        return build_json_error('Email and password are required.', 400)

    user = authenticate(request, username=email, password=password)
    if not user:
        return build_json_error('Invalid email or password.', 401)

    return JsonResponse(build_auth_payload(user))


@csrf_exempt
def google_log_in(request):
    if request.method != 'POST':
        return build_json_error('Method not allowed.', 405)

    payload = parse_json_body(request)
    if payload is None:
        return build_json_error('Invalid JSON payload.', 400)

    credential = str(payload.get('credential') or '').strip()
    if not credential:
        return build_json_error('Google credential is required.', 400)

    try:
        token_payload = verify_google_credential(credential)
        user = get_or_create_google_user(token_payload)
    except ValueError as error:
        return build_json_error(str(error), 400)

    return JsonResponse(build_auth_payload(user))


@csrf_exempt
def log_out(request):
    if request.method != 'POST':
        return build_json_error('Method not allowed.', 405)

    return JsonResponse({'detail': 'Logged out.'})


def account_session(request):
    if request.method != 'GET':
        return build_json_error('Method not allowed.', 405)

    user, error = require_authenticated_user(request)
    if error:
        return error

    return JsonResponse(build_auth_payload(user))


@csrf_exempt
def account_progress(request):
    user, error = require_authenticated_user(request)
    if error:
        return error

    progress_record, _ = UserProgress.objects.get_or_create(user=user)

    if request.method == 'GET':
        return JsonResponse(
            {
                'progress': progress_record.progress,
                'updated_at': progress_record.updated_at.isoformat(),
            }
        )

    if request.method not in {'PUT', 'POST'}:
        return build_json_error('Method not allowed.', 405)

    payload = parse_json_body(request)
    if payload is None:
        return build_json_error('Invalid JSON payload.', 400)

    progress = payload.get('progress')
    if not isinstance(progress, dict):
        return build_json_error('Progress payload must be an object.', 400)

    progress_record.progress = progress
    progress_record.save(update_fields=['progress', 'updated_at'])

    return JsonResponse(
        {
            'progress': progress_record.progress,
            'updated_at': progress_record.updated_at.isoformat(),
        }
    )


@csrf_exempt
def recognize_screenshots(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)

    from .services import merge_updates_into_progress, recognize_screenshots_payload

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

    from .services import store_recognition_feedback

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

    from .services import export_ocr_feedback_dataset

    output_format = request.GET.get('format', 'json')
    payload = export_ocr_feedback_dataset(output_format=output_format)
    if str(output_format).lower() == 'jsonl':
        return HttpResponse(payload, content_type='application/x-ndjson; charset=utf-8')

    return JsonResponse(payload)