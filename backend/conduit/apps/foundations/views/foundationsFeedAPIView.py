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


class FoundationsFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Foundation.objects.all()
    renderer_classes = (FoundationJSONRenderer,)
    foundation_serializer = FoundationSerializer

    def get_queryset(self):
        return Foundation.objects.filter(
            founder__in=self.request.user.profile.follows.all()  # TODO: Before was author__in
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.foundation_serializer(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)
