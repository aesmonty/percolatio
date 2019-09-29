from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    FoundationViewSet, FoundationsFeedAPIView, TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'foundations', FoundationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^foundations/feed/?$', FoundationsFeedAPIView.as_view()),

    url(r'^tags/?$', TagListAPIView.as_view()),
]
