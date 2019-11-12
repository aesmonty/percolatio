from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    FoundationViewSet, FoundationsFeedAPIView,
    TagListAPIView, ProfileFollowAPIView,
    GrantsFeedView, FoundationImageUploadView
)

router = DefaultRouter(trailing_slash=False)
router.register('foundations', FoundationViewSet, base_name='foundations')

app_name = 'foundations'

urlpatterns = [
    path('', include(router.urls)),
    path('foundations/feed/', FoundationsFeedAPIView.as_view(),
         name="foundationFeed"),
    path('foundations/<name>/follow/',
         ProfileFollowAPIView.as_view(), name='follow'),
    path('foundations/<name>/upload/<filename>',
         FoundationImageUploadView.as_view()),
    path('foundations/<name>/grants/feed/', GrantsFeedView.as_view()),
    path('foundations/<name>/grants/feed/', GrantsFeedView.as_view()),
    # path(r'^tags/?$', TagListAPIView.as_view()),
]
