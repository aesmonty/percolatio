from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from conduit.apps.grants.renderers import GrantJSONRenderer
from conduit.apps.grants.models import Grant
from conduit.apps.grants.serializers import GrantSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GrantsFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (GrantJSONRenderer,)
    serializer_class = GrantSerializer

    # @swagger_auto_schema(
    #     responses={
    #         201: openapi.Response(
    #             description='Grant Created',
    #             schema=GrantSerializer(),
    #         ),
    #         404: 'Grant not found',
    #     }
    # )
    def delete(self, request, grantSlug):
        """
        Unfavorite a grant.
        """
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            grant = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound('A Grant with this slug was not found.')

        profile.unfavorite_grant(grant)
        serializer = self.serializer_class(grant, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     responses={
    #         201: openapi.Response(
    #             description='Grant Created',
    #             schema=GrantSerializer(),
    #         ),
    #         404: 'Grant not found',
    #     }
    # )
    def post(self, request, grantSlug):
        """
        Favorite a grant.
        """
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            grant = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound('A Grant with this slug was not found.')

        profile.favorite_grant(grant)
        serializer = self.serializer_class(grant, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
