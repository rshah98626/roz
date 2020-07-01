from django.test import TestCase
from ..models import CustomerProfile, Account


class CustomerProfileModelTest(TestCase):
    def setUp(self):
        self.account_username = 'dummy'
        self.account_email = 'test@test.com'
        self.account_first_name = 'Joe'
        self.account_last_name = 'Blow'
        self.cents = 100

        self.customer_profile = CustomerProfile.objects.create(
            cents=self.cents,
            user=Account.objects.create(
                email=self.account_email,
                username=self.account_username,
                first_name=self.account_first_name,
                last_name=self.account_last_name
            )
        )

    def test_customer_profile_has_correct_user_information(self):
        self.assertEqual(self.customer_profile.user.email, self.account_email)
        self.assertEqual(self.customer_profile.user.first_name, self.account_first_name)
        self.assertEqual(self.customer_profile.user.last_name, self.account_last_name)
        self.assertEqual(self.customer_profile.user.username, self.account_username)

    def test_customer_profile_has_correct_cents(self):
        self.assertEqual(self.customer_profile.cents, self.cents)

    def test_customer_profile_get_dollars(self):
        self.assertEqual(self.customer_profile.get_dollars, self.cents / 100)
