from django.test import TestCase
from users.models import Account
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class ProfileRouteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up first user
        cls.email = "test@data.com"
        cls.username = "mikeWazo"
        cls.password = "hellotwice"
        cls.first_name = "Mike"
        cls.last_name = "Wazowski"

        account = Account.objects.create(
            email=cls.email,
            username=cls.username,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )
        account.set_password(cls.password)
        account.save()

        # set up second user
        cls.other_username = 'mikeWazo2'
        cls.other_email = 'test2@data.com'

        account = Account.objects.create(
            email=cls.other_email,
            username=cls.other_username,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )
        account.set_password(cls.password)
        account.save()

        # other variables
        cls.alternate_username = 'rodMan'
        cls.other_first_name = "Rodney"
        cls.other_last_name = "Smith"
        cls.other_password = "fake_password"

    def setUp(self):
        self.client = APIClient()

        # retrieve an auth token to access route
        response = self.client.post('/api/v1/auth/login/', {'username': self.username, "password": self.password})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['key'])

    def test_email_cannot_change(self):
        data = {'username': self.username, 'email': self.other_email}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['username'], self.username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.first_name)
        self.assertEqual(json['last_name'], self.last_name)

    def test_username_can_change(self):
        data = {'username': self.alternate_username}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['username'], self.alternate_username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.first_name)
        self.assertEqual(json['last_name'], self.last_name)

    def test_username_cannot_change_if_unavailable(self):
        data = {'username': self.other_username}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json['username'][0], "A user with that username already exists.")

    def test_first_name_can_change(self):
        data = {'username': self.username, 'first_name': self.other_first_name}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['username'], self.username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.other_first_name)
        self.assertEqual(json['last_name'], self.last_name)

    def test_last_name_can_change(self):
        data = {'username': self.username, 'last_name': self.other_last_name}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['username'], self.username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.first_name)
        self.assertEqual(json['last_name'], self.other_last_name)

    def test_all_fields_change_except_email(self):
        data = {'username': self.alternate_username, 'first_name': self.other_first_name, 'last_name': self.other_last_name}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['username'], self.alternate_username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.other_first_name)
        self.assertEqual(json['last_name'], self.other_last_name)

    def test_username_must_be_present_to_change(self):
        data = {'first_name': self.other_first_name, 'last_name': self.other_last_name}

        response = self.client.put('/api/v1/auth/user/', data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json['username'][0], "This field is required.")

    def test_cannot_change_password(self):
        data = {'username': self.username, 'password': self.other_password}

        response = self.client.put('/api/v1/auth/user/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        account = Account.objects.get(username=self.username)
        self.assertTrue(account.check_password(self.password))
        self.assertFalse(account.check_password(self.other_password))

    def test_can_get_profile(self):
        response = self.client.get('/api/v1/auth/user/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('pk' in json)
        self.assertEqual(json['username'], self.username)
        self.assertEqual(json['email'], self.email)
        self.assertEqual(json['first_name'], self.first_name)
        self.assertEqual(json['last_name'], self.last_name)


