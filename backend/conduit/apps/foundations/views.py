from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Foundation, Tag
from .renderers import FoundationJSONRenderer
from .serializers import FoundationSerializer, TagSerializer


class FoundationViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    lookup_field = 'name'
    queryset = Foundation.objects.select_related('founder', 'founder__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (FoundationJSONRenderer,)
    serializer_class = FoundationSerializer

    def get_queryset(self):
        queryset = self.queryset

        founder = self.request.query_params.get('founder', None)
        if founder is not None:
            queryset = queryset.filter(founder__user__username=founder)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        return queryset

    def create(self, request):
        serializer_context = {
            'founder': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('foundation', {})

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

    def retrieve(self, request, name):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, name):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')
            
        serializer_data = request.data.get('foundation', {})

        serializer = self.serializer_class(
            serializer_instance, 
            context=serializer_context,
            data=serializer_data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ArticlesFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Foundation.objects.all()
    renderer_classes = (FoundationJSONRenderer,)
    serializer_class = FoundationSerializer

    def get_queryset(self):
        return Foundation.objects.filter(
            founder__in=self.request.user.profile.follows.all() # TODO: Before was author__in
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)
