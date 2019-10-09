from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Foundation, Tag
from ..renderers import FoundationJSONRenderer
from ..serializers import FoundationSerializer, TagSerializer


class FoundationViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    lookup_field = 'name'
    queryset = Foundation.objects.select_related('founder', 'founder__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (FoundationJSONRenderer,)
    foundation_serializer = FoundationSerializer

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
        context = {
            'founder': request.user.profile,
            'request': request
        }

        foundation = request.data.get('foundation', {})
        foundation_serialized = self.foundation_serializer(
            data=foundation, context=context
        )

        # TODO: Error when we create foundations with same name

        foundation_serialized.is_valid(raise_exception=True)
        foundation_serialized.save()
        return Response(foundation_serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.foundation_serializer(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, name):
        context = {'request': request}

        try:
            foundation = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')

        foundation_serialized = self.foundation_serializer(
            foundation,
            context=context
        )

        return Response(foundation_serialized.data, status=status.HTTP_200_OK)

    def update(self, request, name):
        context = {'request': request}

        try:
            original_foundation = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')

        new_foundation = request.data.get('foundation', {})

        serializer = self.foundation_serializer(
            original_foundation,
            context=context,
            data=new_foundation,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
