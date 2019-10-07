from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..renderers import ProfileJSONRenderer
from conduit.apps.foundations.renderers import FoundationJSONRenderer
from conduit.apps.foundations.serializers import FoundationSerializer


class FollowingAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (FoundationJSONRenderer,)
    foundation_serializer = FoundationSerializer

    def retrieve(self, request, username, *args, **kwargs):
        queryset = self.get_queryset(username)
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.foundation_serializer(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)

    def get_queryset(self, username):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        return profile.follows_foundation.all()
