from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    GrantViewSet, GrantsFavoriteAPIView, GrantsFeedAPIView,
    TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'grants', GrantViewSet)

app_name = 'grants'

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^grants/feed/?$', GrantsFeedAPIView.as_view()),

    url(r'^grants/(?P<grant_slug>[-\w]+)/favorite/?$',
        GrantsFavoriteAPIView.as_view()),

    url(r'^tags/?$', TagListAPIView.as_view()),
]
