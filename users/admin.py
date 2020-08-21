#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account, CustomerProfile


class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = ['email', 'username', 'first_name', 'last_name', 'password']


admin.site.register(Account, AccountAdmin)
admin.site.register(CustomerProfile)
