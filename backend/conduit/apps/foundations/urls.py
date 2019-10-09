from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    FoundationViewSet, FoundationsFeedAPIView, TagListAPIView, ProfileFollowAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'foundations', FoundationViewSet)

app_name = 'foundations'

urlpatterns = [
    path('', include(router.urls)),
    path('foundations/feed/', FoundationsFeedAPIView.as_view()),
    path('foundations/<name>/follow/', ProfileFollowAPIView.as_view()),
    # path(r'^tags/?$', TagListAPIView.as_view()),
]
