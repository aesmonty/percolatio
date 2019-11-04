from rest_framework import generics, mixins, status, viewsets, permissions
from rest_framework.exceptions import NotFound, ParseError, AuthenticationFailed
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
)
from rest_framework.response import Response
from rest_framework.views import APIView

from conduit.apps.foundations.models import Foundation, Tag
from conduit.apps.foundations.renderers import FoundationJSONRenderer
from conduit.apps.foundations.serializers import FoundationSerializer, TagSerializer

from conduit.apps.grants.renderers import GrantJSONRenderer
from conduit.apps.grants.models import Grant, GrantApplication
from conduit.apps.grants.serializers import GrantSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


FOUDNATION_DOCUMENTATION_SCHEMA = {'Foundation': openapi.Schema(type=openapi.TYPE_OBJECT, description='Foundation',
                                                                properties={
                                                                    'Name': openapi.Schema(type=openapi.TYPE_STRING, description="Foundation Name")
                                                                }),
                                   }


GRANT_DOCUMENTATION_SCHEMA = {'Grant': openapi.Schema(type=openapi.TYPE_OBJECT, description='Foundation',
                                                      required=[
                                                          'title', 'amountPerGrantee', 'applicationsStartDate', 'applicationsEndDate', 'description'],
                                                      properties={
                                                          'title': openapi.Schema(type=openapi.TYPE_STRING, description="Grant Name"),
                                                          'tagList': openapi.Schema(type=openapi.TYPE_ARRAY, description="Grant Tags", items=openapi.Items(type=openapi.TYPE_STRING)),
                                                          'isPreFunded': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is the grant pre funded by the foundation"),
                                                          'numberOfGrantees': openapi.Schema(type=openapi.TYPE_INTEGER, default=1, description="Number of people who can win the grant"),
                                                          "amountPerGrantee": openapi.Schema(type=openapi.TYPE_INTEGER, description="Amount of money awarded to each grant winner"),
                                                          "nonFinancialRewards": openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False, description="Other rewards"),
                                                          "applicationsStartDate": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="When can applicants start applying to a grant"),
                                                          "applicationsEndDate": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="When the grant will stop receiving applications"),
                                                          "description": openapi.Schema(type=openapi.TYPE_STRING, description="Grant Description"),
                                                          "externalWebsite": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Other website associated with the grant"),
                                                          "otherDetails": openapi.Schema(type=openapi.TYPE_STRING, description="Other details for the grant"),
                                                      })
                              }


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.founder.user == request.user


class GrantsViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    # lookup_field = 'name'
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Foundation.objects.all()
    renderer_classes = (GrantJSONRenderer,)
    grant_serializer = GrantSerializer
    foundation_serializer = FoundationSerializer

    def get_querysets(self, foundations_name, pk):
        try:
            foundation = Foundation.objects.get(
                name=foundations_name)
        except Foundation.DoesNotExist:
            raise NotFound(
                "A foundation with name: {} does not exist.".format(foundations_name))

        try:
            grant = Grant.objects.get(slug=pk)
        except Grant.DoesNotExist:
            raise NotFound(
                "A grant with slug equal to {} does not exist.".format(pk))

        return foundation, grant

    def list(self, request):
        """
        List grants with filters
        """
        queryset = Grant.objects.select_related(
            'foundation', 'foundation__founder__user')

        founder = self.request.query_params.get('founder', None)
        if founder is not None:
            queryset = queryset.filter(
                foundation__founder__user__username=founder)

        favorited_by = self.request.query_params.get('favorited', None)
        if favorited_by is not None:
            queryset = queryset.filter(
                favorited_grants_by__user__username=favorited_by
            )

        applied_to = self.request.query_params.get('applicant', None)
        if applied_to is not None:
            queryset = Grant.objects.filter(
                applicants__author__user__username=applied_to
            )

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.grant_serializer(
            page, context=serializer_context, many=True
        )
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            **FOUDNATION_DOCUMENTATION_SCHEMA,
            **GRANT_DOCUMENTATION_SCHEMA
        }
    ), responses={404: 'Foundation not found', 403: 'Not Authorized'})
    def create(self, request):
        """
        Create a grant from a foundation
        ---
        """

        foundation = request.data.get('Foundation', None)

        if foundation is None or foundation["Name"] is None:
            raise ParseError("Could not parse foundation name")

        foundations_name = foundation["Name"]

        try:
            foundation = Foundation.objects.get(
                name=foundations_name)
        except Foundation.DoesNotExist:
            raise NotFound(
                "A foundation with name: {} does not exist.".format(foundations_name))

        self.check_object_permissions(self.request, foundation)

        grant = request.data.get('Grant', {})
        serializer_context = {
            'foundation': foundation,
            'request': request
        }

        grant_serialized_data = self.grant_serializer(
            data=grant,
            context=serializer_context
        )

        grant_serialized_data.is_valid(raise_exception=True)
        grant_serialized_data.save()
        return Response(grant_serialized_data.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=FOUDNATION_DOCUMENTATION_SCHEMA,
    ), responses={404: 'Foundation not found', 403: 'Not Authorized'})
    def delete(self, request, pk):
        """
        Delete a grant
        """

        foundation = request.data.get('Foundation', None)
        if foundation is None or foundation["Name"] is None:
            raise ParseError("Could not parse foundation name")

        foundations_name = foundation["Name"]
        foundation, grant = self.get_querysets(foundations_name, pk)
        self.check_object_permissions(self.request, foundation)
        serializer_context = {
            'foundation': foundation,
            'request': request
        }

        grant_serialized_data = self.grant_serializer(
            grant,
            context=serializer_context
        )

        grant.delete()
        return Response(grant_serialized_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        Retrieve a grant
        """
        try:
            grant = Grant.objects.get(slug=pk)
        except Grant.DoesNotExist:
            raise NotFound(
                "A grant with slug equal to {} does not exist.".format(pk))

        serializer_context = {
            'foundation': grant.foundation,
            'request': request
        }

        grant_serialized_data = self.grant_serializer(
            grant,
            context=serializer_context
        )
        return Response(grant_serialized_data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=FOUDNATION_DOCUMENTATION_SCHEMA,
    ), responses={404: 'Foundation not found', 403: 'Not Authorized'})
    def update(self, request, pk):
        """
        Update a grant
        """
        foundation = request.data.get('Foundation', None)

        if foundation is None or foundation["Name"] is None:
            raise ParseError("Could not parse foundation name")

        foundations_name = foundation["Name"]
        foundation, grant = self.get_querysets(foundations_name, pk)
        self.check_object_permissions(self.request, foundation)

        serializer_context = {
            'foundation': foundation,
            'request': request
        }

        new_grant = request.data.get('Grant', {})
        # TODO: We should be stricter here. We may want to have fields that are read only and that we should not be able to update
        serializer = self.grant_serializer(
            grant,
            context=serializer_context,
            data=new_grant,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
