from django.test import TestCase, Client
from users.models import Account, CustomerProfile


class RegisterRouteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_email = "test@data.com"
        cls.first_username = "mikeWazo"

        cls.new_username = "rahulshah"
        cls.new_email = "hello@gmail.com"

        cls.password = "hellotwice"
        cls.first_name = "Mike"
        cls.last_name = "Wazowski"

        account = Account.objects.create(
            email=cls.first_email,
            username=cls.first_username,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )
        account.set_password(cls.password)
        account.save()

    def setUp(self):
        self.client = Client()

    @staticmethod
    def successful_response(response):
        return 'key' in response.json().keys()

    def test_register_works(self):
        data = {
            'username': self.new_username, 'first_name': self.first_name, 'last_name': self.last_name,
            'email': self.new_email, 'password': self.password, 'password2': self.password
        }

        # make request and verify it was successful
        response = self.client.post('/api/v1/auth/registration/', data)
        self.assertTrue(self.successful_response(response))

        # verify a customer profile was created to be associated with the new account
        account = Account.objects.latest('id')
        customer_profile = CustomerProfile.objects.latest('id')
        self.assertTrue(account)
        self.assertTrue(customer_profile.user, account)
        self.assertEqual(customer_profile.cents, 100000)  # initial amount of cash in a CustomerProfile

    def test_reject_user_if_passwords_do_not_match(self):
        data = {
            'username': self.new_username, 'first_name': self.first_name, 'last_name': self.last_name,
            'email': self.new_email, 'password': self.password, 'password2': "passwords_do_not_match"
        }

        response = self.client.post('/api/v1/auth/registration/', data)
        self.assertFalse(self.successful_response(response))
        self.assertEqual(response.json()['password'], 'Passwords must match.')

    def test_email_can_be_used_only_once(self):
        data = {
            'username': self.new_username, 'first_name': self.first_name, 'last_name': self.last_name,
            'email': self.first_email, 'password': self.password, 'password2': self.password
        }

        response = self.client.post('/api/v1/auth/registration/', data)
        self.assertFalse(self.successful_response(response))
        self.assertEqual(response.json()['email'], 'Email is already in use.')

    def test_username_can_be_used_only_once(self):
        data = {
            'username': self.first_username, 'first_name': self.first_name, 'last_name': self.last_name,
            'email': self.new_email, 'password': self.password, 'password2': self.password
        }

        response = self.client.post('/api/v1/auth/registration/', data)
        self.assertFalse(self.successful_response(response))
        self.assertEqual(response.json()['username'], ['A user with that username already exists.'])
