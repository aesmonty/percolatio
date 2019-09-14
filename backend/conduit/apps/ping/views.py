from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class PingAPIView(RetrieveAPIView):
    def retrieve(self, request):
        return Response({'Hello': 'World'}, status=HTTP_200_OK)
