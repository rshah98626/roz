#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework.test import APIClient, APITestCase
from chatty.views import FeedView
from users.models import Account


class FeedViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account(
            emal="hi@cmail.com",
            username="man",
            first_name="sara",
            last_name="smith"
        )
        cls.user.set_password("hihihihi2")
        cls.user.save()

    def setUp(self):
        self.client = APIClient()
        self.testable_view = FeedView.as_view()
        self.client.force_authenticate(user=self.user)

