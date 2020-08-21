#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.contrib.auth.forms import UserChangeForm
from users.models.account import Account


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = UserChangeForm.Meta.fields
