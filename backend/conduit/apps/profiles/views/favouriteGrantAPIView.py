from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..renderers import ProfileJSONRenderer
from ..serializers import ProfileSerializer


class FavouriteGrantAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer,)
    profile_serializer = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        # TODO: implement this :)
        raise NotImplementedError(
            "This part of the API is not implemented yet :(")
