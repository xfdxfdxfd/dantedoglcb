from django.urls import path

from .views import export_recognition_feedback, healthcheck, recognize_screenshots, record_recognition_feedback


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('sync/recognize/', recognize_screenshots, name='recognize-screenshots'),
    path('sync/feedback/', record_recognition_feedback, name='record-recognition-feedback'),
    path('sync/feedback/export/', export_recognition_feedback, name='export-recognition-feedback'),
]