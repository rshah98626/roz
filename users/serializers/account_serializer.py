#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework.serializers import ModelSerializer
from users.models.account import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
