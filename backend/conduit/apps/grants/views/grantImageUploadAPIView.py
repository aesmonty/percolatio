from rest_framework import generics, mixins, status, viewsets, permissions
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (BasePermission)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Grant
from rest_framework.parsers import FileUploadParser


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.founder.user == request.user


class GrantImageUploadView(APIView):
    queryset = Grant.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (FileUploadParser, )

    def put(self, request, filename, grantSlug):
        try:
            grant = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound(
                "A grant with slug equal to {} does not exist.".format(pk))

        self.check_object_permissions(self.request, grant.foundation)
        grant_image = request.data['file']
        grant.img = grant_image
        grant.save()
        return Response(status=204)

    def delete(self, request, filename, grantSlug):

        try:
            grant = Grant.objects.get(slug=grantSlug)
        except Grant.DoesNotExist:
            raise NotFound(
                "A grant with slug equal to {} does not exist.".format(pk))

        self.check_object_permissions(self.request, grant.foundation)
        grant.img.delete(save=False)
        grant.save()
        return Response(status=204)
