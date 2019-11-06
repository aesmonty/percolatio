from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (BasePermission)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Grant, GrantApplication
from ..serializers import GrantSerializer, GrantApplicationSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAuthorizedOrIsMethodSafe(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.foundation.founder.user == request.user


class ApplicantsListAPIView(generics.ListCreateAPIView):

    lookup_field = 'grant__slug'
    lookup_url_kwarg = 'grant_slug'
    permission_classes = (IsAuthorizedOrIsMethodSafe,)
    serializer_class = GrantApplicationSerializer
    queryset = GrantApplication.objects.all()

    def list(self, request, grantSlug):
        """
        List all applicants in a grant
        """

        try:
            grant = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound(
                "A grant with slug equal to {} does not exist.".format(grantSlug))

        self.check_object_permissions(self.request, grant)
        applicants = self.queryset.filter(grant__slug=grantSlug)

        page = self.paginate_queryset(applicants)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description='Application Created',
                schema=GrantApplicationSerializer(),
            ),
            404: 'Grant not found',
        }
    )
    def create(self, request, grantSlug):
        """
        Apply to a grant
        """

        data = request.data.get('application', None)

        if data is None:
            raise ParseError(
                "Could not parse application object in the request")

        context = {'author': request.user.profile}
        try:
            context['grant'] = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound(
                'Could not find a grant with slug {}'.format(grantSlug))

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
