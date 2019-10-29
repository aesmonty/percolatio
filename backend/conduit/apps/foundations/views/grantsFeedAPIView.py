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

from conduit.apps.grants.renderers import GrantJSONRenderer
from conduit.apps.grants.serializers import GrantSerializer


class GrantsFeedView(generics.ListAPIView):
    queryset = Foundation.objects.all()
    renderer_classes = (GrantJSONRenderer,)
    grant_serializer = GrantSerializer

    def get_queryset(self, foundation_name):

        try:
            foundation = self.queryset.get(name=foundation_name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this username does not exist.')

        return foundation.grants.all()

    def list(self, request, name):

        queryset = self.get_queryset(name)
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.grant_serializer(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)
