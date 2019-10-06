from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet, ArticlesFavoriteAPIView, ArticlesFeedAPIView,
    CommentsListCreateAPIView, CommentsDestroyAPIView, TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

app_name = 'articles'

urlpatterns = [
    path('', include(router.urls)),

    path('articles/feed/', ArticlesFeedAPIView.as_view()),

    path('articles/<slug:title>/favorite/',
         ArticlesFavoriteAPIView.as_view()),

    path('articles/<slug:title>/comments/',
         CommentsListCreateAPIView.as_view()),

    path('articles/<slug:title>/comments/we',  # TODO: this url probably incorrect but who cares this going to be deleted
         CommentsDestroyAPIView.as_view()),

    path('tags/', TagListAPIView.as_view()),
]
