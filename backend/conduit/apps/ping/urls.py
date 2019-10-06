from django.urls import path

from .views import PingAPIView

app_name = 'ping'

urlpatterns = [
    path('', PingAPIView.as_view())
]
