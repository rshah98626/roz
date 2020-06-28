from rest_framework import viewsets
from ..models import Account
from ..serializers import AccountSerializer


class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer