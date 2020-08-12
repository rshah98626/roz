#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.contrib.auth.forms import UserCreationForm
from users.models.account import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = UserCreationForm.Meta.fields
