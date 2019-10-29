
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Grant, GrantApplication
from ..serializers import GrantSerializer, GrantApplicationSerializer


class IsApplicationOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user


class ApplicationDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsApplicationOwner,)
    serializer_class = GrantApplicationSerializer
    queryset = GrantApplication.objects.all()

    def destroy(self, request, grantSlug, id):
        """
        Withdraw application from a grant.
        """
        try:
            grantApplication = self.queryset.get(id=id)
        except GrantApplication.DoesNotExist:
            raise NotFound('A grantApplication with this ID does not exist.')

        self.check_object_permissions(self.request, grantApplication)
        # NOTE: Maybe instead of deleting we should be cheating and keep the data instead.
        grantApplication.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
