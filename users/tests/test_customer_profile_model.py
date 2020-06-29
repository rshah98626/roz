from django.test import TestCase
from ..models import CustomerProfile, Account


class CustomerProfileModelTest(TestCase):
    def setUp(self):
        CustomerProfile.objects.create(
            cents=100,
            user=Account.objects.create(
                email='test@test.com',
                username='dummy',
                first_name='Joe',
                last_name='Blow'
            )
        )

    def test_customer_profile_has_correct_user(self):
        profile = CustomerProfile.objects.get(cents=100)
        account = Account.objects.get(username='dummy')
        self.assertEqual(profile.user, account)

    def test_customer_profile_has_correct_cents(self):
        profile = CustomerProfile.objects.get(cents=100)
        self.assertEqual(profile.cents, 100)

    def test_customer_profile_get_dollars(self):
        profile = CustomerProfile.objects.get(cents=100)
        self.assertEqual(profile.get_dollars, 1)
