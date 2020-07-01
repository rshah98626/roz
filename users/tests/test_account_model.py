from django.test import TestCase
from ..models import Account


class AccountModelTest(TestCase):
    def setUp(self):
        self.username = 'dummy'
        self.email = 'test@test.com'
        self.first_name = 'Mike'
        self.last_name = 'Wazowski'
        self.password = 'mikeWazo'

        self.account = Account.objects.create(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name
        )

        self.account.set_password(self.password)

    def test_account_has_correct_information(self):
        self.assertEqual(self.account.email, self.email)
        self.assertEqual(self.account.first_name, self.first_name)
        self.assertEqual(self.account.last_name, self.last_name)
        self.assertEqual(self.account.username, self.username)

    def test_account_has_correct_password(self):
        self.assertTrue(self.account.check_password(self.password))
        self.assertFalse(self.account.check_password('hiya'))
