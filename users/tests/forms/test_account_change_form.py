#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from users.forms import AccountChangeForm
from users.models import Account


class AccountChangeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create(
            email="test@data.com",
            username="mikeWazo",
            first_name="Mike",
            last_name="Wazowski",
        )
        account.set_password("himynameisrahul")
        account.save()

    def test_field_labels(self):
        form = AccountChangeForm()
        self.assertEqual(form.fields['username'].label, "Username")
        self.assertEqual(form.fields['password'].label, "Password")
        self.assertEqual(form.fields['last_login'].label, "Last login")
        self.assertEqual(form.fields['is_superuser'].label, "Superuser status")
        self.assertEqual(form.fields['groups'].label, "Groups")
        self.assertEqual(form.fields['user_permissions'].label, "User permissions")
        self.assertEqual(form.fields['first_name'].label, "First name")
        self.assertEqual(form.fields['last_name'].label, "Last name")
        self.assertEqual(form.fields['email'].label, "Email address")
        self.assertEqual(form.fields['is_staff'].label, "Staff status")
        self.assertEqual(form.fields['is_active'].label, "Active")
        self.assertEqual(form.fields['date_joined'].label, "Date joined")
