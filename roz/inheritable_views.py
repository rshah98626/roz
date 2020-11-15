#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework.views import APIView
from rest_framework import authentication, permissions


class AuthenticatedView(APIView):
    """
    A base view which mandates access to only authenticated users.
    """
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )