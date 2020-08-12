#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from users.models.account import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
