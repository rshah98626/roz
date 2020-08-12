#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from users.forms import AccountCreationForm
from users.models import Account


class AccountCreationFormTest(TestCase):
    username = "mikeWazo"
    new_password = "himynameisrahul"
    new_username = "temp"

    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create(
            email="test@data.com",
            username=cls.username,
            first_name="Mike",
            last_name="Wazowski"
        )
        account.set_password("mikeWazowski")
        account.save()

    def test_field_labels(self):
        form = AccountCreationForm()
        self.assertEqual(form.fields['username'].label, "Username")
        self.assertEqual(form.fields['password1'].label, "Password")
        self.assertEqual(form.fields['password2'].label, "Password confirmation")

    def test_create_user(self):
        form = AccountCreationForm(data={
            'username': self.new_username,
            'password1': self.new_password,
            'password2': self.new_password
        })
        self.assertTrue(form.is_valid())
        form.save()

        account = Account.objects.latest('id')
        self.assertEqual(account.username, self.new_username)
        self.assertTrue(account.check_password(self.new_password))

    def test_invalid_username(self):
        form = AccountCreationForm(data={
            'username': self.username,
            'password1': self.new_password,
            'password2': self.new_password
        })
        self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        form = AccountCreationForm(data={
            'username': self.new_username,
            'password1': 'random',
            'password2': self.new_password
        })
        self.assertFalse(form.is_valid())

    def test_no_password(self):
        form = AccountCreationForm(data={
            'username': self.new_username,
            'password1': '',
            'password2': ''
        })
        self.assertFalse(form.is_valid())

    def test_no_username(self):
        form = AccountCreationForm(data={
            'username': '',
            'password1': self.new_password,
            'password2': self.new_password
        })
        self.assertFalse(form.is_valid())

    def test_all_fields_empty(self):
        form = AccountCreationForm(data={
            'username': '',
            'password1': '',
            'password2': ''
        })
        self.assertFalse(form.is_valid())
