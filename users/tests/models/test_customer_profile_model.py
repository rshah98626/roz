#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from users.models import CustomerProfile, Account


class CustomerProfileModelTest(TestCase):
    account_username = 'dummy'
    account_email = 'test@test.com'
    account_first_name = 'Joe'
    account_last_name = 'Blow'
    cents = 100

    @classmethod
    def setUpTestData(cls):
        CustomerProfile.objects.create(
            cents=cls.cents,
            user=Account.objects.create(
                email=cls.account_email,
                username=cls.account_username,
                first_name=cls.account_first_name,
                last_name=cls.account_last_name
            )
        )

    def test_customer_profile_has_correct_user_information(self):
        customer_profile = CustomerProfile.objects.latest('id')
        self.assertEqual(customer_profile.user.email, self.account_email)
        self.assertEqual(customer_profile.user.first_name, self.account_first_name)
        self.assertEqual(customer_profile.user.last_name, self.account_last_name)
        self.assertEqual(customer_profile.user.username, self.account_username)

    def test_customer_profile_has_correct_cents(self):
        customer_profile = CustomerProfile.objects.latest('id')
        self.assertEqual(customer_profile.cents, self.cents)

    def test_customer_profile_cash(self):
        customer_profile = CustomerProfile.objects.latest('id')
        self.assertEqual(customer_profile.cash, self.cents / 100)

    def test_field_labels(self):
        customer_profile = CustomerProfile.objects.latest('id')
        self.assertEqual(customer_profile._meta.get_field('cents').verbose_name, 'money in the account (cents)')
        self.assertEqual(customer_profile._meta.get_field('user').verbose_name, 'user')
