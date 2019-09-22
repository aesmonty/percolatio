from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Grant, Tag
from .renderers import GrantJSONRenderer
from .serializers import GrantSerializer, TagSerializer


class GrantViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = Grant.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (GrantJSONRenderer,)
    serializer_class = GrantSerializer

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__username=author)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get('favorited', None)
        if favorited_by is not None:
            queryset = queryset.filter(
                favorited_by__user__username=favorited_by
            )

        return queryset

    def create(self, request):
        serializer_context = {
            'author': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Grant.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Grant.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GrantsFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (GrantJSONRenderer,)
    serializer_class = GrantSerializer

    def delete(self, request, article_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            grant = Grant.objects.get(slug=article_slug)
        except Grant.DoesNotExist:
            raise NotFound('A grant with this slug was not found.')

        profile.unfavorite(grant)

        serializer = self.serializer_class(grant, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            grant = Grant.objects.get(slug=article_slug)
        except Grant.DoesNotExist:
            raise NotFound('A grant with this slug was not found.')

        profile.favorite(grant)

        serializer = self.serializer_class(grant, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)


class GrantsFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Grant.objects.all()
    renderer_classes = (GrantJSONRenderer,)
    serializer_class = GrantSerializer

    def get_queryset(self):
        return Grant.objects.filter(
            author__in=self.request.user.profile.follows.all()
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)
