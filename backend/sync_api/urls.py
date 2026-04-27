from django.urls import path

from .views import healthcheck, recognize_screenshots


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('sync/recognize/', recognize_screenshots, name='recognize-screenshots'),
]