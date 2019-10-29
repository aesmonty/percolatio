from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from conduit.apps.grants.models import Grant, Tag
from conduit.apps.grants.renderers import GrantJSONRenderer
from conduit.apps.grants.serializers import GrantSerializer


class GrantsFeedView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Grant.objects.all()
    renderer_classes = (GrantJSONRenderer,)
    grant_serializer = GrantSerializer

    def list(self, request):
        """
        List all grants.
        """
        page = self.paginate_queryset(self.queryset)

        serializer_context = {'request': request}
        serializer = self.grant_serializer(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)
