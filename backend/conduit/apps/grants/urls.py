from django.conf.urls import include, url
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    GrantsViewSet,
    GrantsFeedView,
    GrantsFavoriteAPIView,
    ApplicantsListAPIView, ApplicationDestroyAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register('grants', GrantsViewSet, base_name='grants')

app_name = 'grants'

urlpatterns = [
    path('', include(router.urls)),

    url('grants/feed/', GrantsFeedView.as_view()),

    path('grants/<slug:grantSlug>/favorite/',
         GrantsFavoriteAPIView.as_view(), name='grantFavorite'),
    path('grants/<slug:grantSlug>/applicants/<int:id>/',
         ApplicationDestroyAPIView.as_view(), name='applicationDestroy'),
    path('grants/<slug:grantSlug>/applicants/',
         ApplicantsListAPIView.as_view(), name='applicationCreate'),
    # url(r'^tags/?$', TagListAPIView.as_view()),
]
