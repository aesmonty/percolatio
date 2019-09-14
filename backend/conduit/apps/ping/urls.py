from django.conf.urls import url

from .views import PingAPIView

urlpatterns = [
    url('', PingAPIView.as_view())
]
