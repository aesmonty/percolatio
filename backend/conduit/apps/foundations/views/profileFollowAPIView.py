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


class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FoundationJSONRenderer,)
    foundation_serializer = FoundationSerializer

    def __validate_input(self, request, name):
        if name is None or name.isspace():
            raise ParseError("foundation name cannot be null or whitespace")

        if self.request.user is None or self.request.user.profile is None:
            raise ParseError("Request must contain a user with a profile")

    def delete(self, request, name):

        self.__validate_input(request, name)
        try:
            # TODO: Not sure about his inside ()
            foundation = Foundation.objects.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name was not found.')

        follower = self.request.user.profile
        follower.unfollow_foundation(foundation)

        serializer = self.foundation_serializer(foundation, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, name):

        self.__validate_input(request, name)
        try:
            foundation = Foundation.objects.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name was not found.')

        follower = self.request.user.profile
        follower.follow_foundation(foundation)

        serializer = self.foundation_serializer(foundation, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)
