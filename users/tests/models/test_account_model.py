from django.test import TestCase
from users.models import Account


class AccountModelTest(TestCase):
    username = 'dummy'
    email = 'test@test.com'
    first_name = 'Mike'
    last_name = 'Wazowski'
    password = 'mikeWazo'

    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create(
            email=cls.email,
            username=cls.username,
            first_name=cls.first_name,
            last_name=cls.last_name
        )

        account.set_password(cls.password)
        account.save()

    def test_account_has_correct_information(self):
        account = Account.objects.latest('id')
        self.assertEqual(account.email, self.email)
        self.assertEqual(account.first_name, self.first_name)
        self.assertEqual(account.last_name, self.last_name)
        self.assertEqual(account.username, self.username)

    def test_account_has_correct_password(self):
        account = Account.objects.latest('id')
        self.assertTrue(account.check_password(self.password))
        self.assertFalse(account.check_password('hiya'))

    def test_field_labels(self):
        account = Account.objects.latest('id')
        self.assertEquals(account._meta.get_field('email').verbose_name, 'email address')
        self.assertEquals(account._meta.get_field('username').verbose_name, 'username')
        self.assertEquals(account._meta.get_field('last_name').verbose_name, 'last name')
        self.assertEquals(account._meta.get_field('first_name').verbose_name, 'first name')
        self.assertEquals(account._meta.get_field('password').verbose_name, 'password')

