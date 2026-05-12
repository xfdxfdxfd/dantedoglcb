from django.urls import path

from .views import (
    account_progress,
    account_session,
    export_recognition_feedback,
    google_log_in,
    healthcheck,
    log_in,
    log_out,
    recognize_screenshots,
    record_recognition_feedback,
    sign_up,
)


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('auth/google/', google_log_in, name='google-log-in'),
    path('auth/signup/', sign_up, name='sign-up'),
    path('auth/login/', log_in, name='log-in'),
    path('auth/logout/', log_out, name='log-out'),
    path('auth/session/', account_session, name='account-session'),
    path('account/progress/', account_progress, name='account-progress'),
    path('sync/recognize/', recognize_screenshots, name='recognize-screenshots'),
    path('sync/feedback/', record_recognition_feedback, name='record-recognition-feedback'),
    path('sync/feedback/export/', export_recognition_feedback, name='export-recognition-feedback'),
]