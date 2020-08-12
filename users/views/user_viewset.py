"""
This viewset is deprecated, but it's a good example of how views should be modeled as
"""

#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from ..serializers import AccountSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    elif request.method == 'POST':
        # TODO make this serializer check for email & username
        serializer = AccountSerializer(request.user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
