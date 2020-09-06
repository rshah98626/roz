#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase, Client
from users.models import Account


class LoginRouteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@data.com"
        cls.username = "mikeWazo"
        cls.password = "hellotwice"
        cls.first_name = "Mike"
        cls.last_name = "Wazowski"

        cls.false_password = 'that_is_not_the_password'
        cls.false_username = 'not_a_real_username'

        account = Account(
            email=cls.email,
            username=cls.username,
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

    @staticmethod
    def unsuccessful_response(response):
        resp = response.json()
        return 'key' not in resp.keys() and resp['non_field_errors'] == ['Unable to log in with provided credentials.']

    def test_login_works(self):
        data = {'username': self.username, 'password': self.password}

        # make request and verify it was successful
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertTrue(self.successful_response(response))

    def test_reject_login_if_passwords_do_not_match(self):
        data = {'username': self.username, 'password': self.false_password}

        response = self.client.post('/api/v1/auth/login/', data)
        self.assertTrue(self.unsuccessful_response(response))

    def test_reject_unknown_username(self):
        data = {'username': self.false_username, 'password': self.password}

        response = self.client.post('/api/v1/auth/login/', data)
        self.assertTrue(self.unsuccessful_response(response))
