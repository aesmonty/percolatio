from rest_framework import generics, mixins, status, viewsets, permissions
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (BasePermission)
from rest_framework.response import Response
from rest_framework.views import APIView

from .foundationPermissions import IsFoundationOwnerOrReadOnly
from ..models import Foundation
from rest_framework.parsers import FileUploadParser


class FoundationImageUploadView(APIView):
    queryset = Foundation.objects.all()
    permission_classes = (IsFoundationOwnerOrReadOnly,)
    parser_classes = (FileUploadParser, )

    def put(self, request, filename, name):

        try:
            foundation = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')

        self.check_object_permissions(self.request, foundation)
        foundation_image = request.data['file']
        foundation.img = foundation_image
        foundation.save()
        return Response(status=204)

    def delete(self, request, filename, name):

        try:
            foundation = self.queryset.get(name=name)
        except Foundation.DoesNotExist:
            raise NotFound('A foundation with this name does not exist.')

        self.check_object_permissions(self.request, foundation)

        foundation.img.delete(save=False)
        foundation.save()
        return Response(status=204)
