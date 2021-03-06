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
    serializer_class = FoundationSerializer

    def retrieve(self, request, username, *args, **kwargs):
        # NOTE: This query set can easily be modified to return only the foundations
        #       that the profile owns. This could either be a parameter in this request or a new endpoint.
        queryset = self.get_queryset(username)
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)

    def get_queryset(self, username):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        return profile.follows_foundation.all()
