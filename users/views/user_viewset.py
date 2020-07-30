from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from ..serializers import AccountSerializer


class UserViewset(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Returns the information for a given user
        """
        return Response({'user': request.user})

    @classmethod
    def get_extra_actions(cls):
        return []


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    return Response({'user': AccountSerializer(request.user).data})
