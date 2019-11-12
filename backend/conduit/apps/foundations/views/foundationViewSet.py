from rest_framework import generics, mixins, status, viewsets, permissions
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (BasePermission)
from rest_framework.response import Response
from rest_framework.views import APIView

from .foundationPermissions import IsFoundationOwnerOrReadOnly
from ..models import Foundation, Tag
from ..renderers import FoundationJSONRenderer
from ..serializers import FoundationSerializer, TagSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


FOUDNATION_DOCUMENTATION_SCHEMA = {'Foundation': openapi.Schema(type=openapi.TYPE_OBJECT, description='Foundation',
                                                                properties={
                                                                    'Name': openapi.Schema(type=openapi.TYPE_STRING, description="Foundation Name")
                                                                }),
                                   'Description': openapi.Schema(type=openapi.TYPE_OBJECT, description='A description for the foundation',
                                                                 properties={
                                                                     'Name': openapi.Schema(type=openapi.TYPE_STRING, description="Foundation Name")
                                                                 }),
                                   }


class FoundationViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    lookup_field = 'name'
    queryset = Foundation.objects.select_related('founder', 'founder__user')
    permission_classes = (IsFoundationOwnerOrReadOnly,)
    renderer_classes = (FoundationJSONRenderer,)
    foundation_serializer = FoundationSerializer
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

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=FOUDNATION_DOCUMENTATION_SCHEMA),
        responses={
        404: 'Incorrect body',
        403: 'Not Authorized'})
    def create(self, request):

        context = {
            'founder': request.user.profile,
            'request': request
        }

        foundation = request.data.get('foundation', None)
        if foundation is None:
            raise ParseError("Cannot find foundation object in the request")

        foundation_serialized = self.foundation_serializer(
            data=foundation, context=context
        )

        foundation_serialized.is_valid(raise_exception=True)
        foundation_serialized.save()
        return Response(foundation_serialized.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(manual_parameters=[
                         openapi.Parameter(
                             'founder', openapi.IN_QUERY,  description='Select foundations based on the founder',  type=openapi.TYPE_STRING, example="davinci"),
                         ])
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

        self.check_object_permissions(self.request, original_foundation)
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
