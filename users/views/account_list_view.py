#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import viewsets
from ..models import Account
from ..serializers import AccountSerializer


class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
