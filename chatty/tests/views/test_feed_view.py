#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from chatty.models import Post, Fund
from users.models import Account


class FeedViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account(
            email="hi@cmail.com",
            username="man",
            first_name="sara",
            last_name="smith"
        )
        cls.user.set_password("hihihihi2")
        cls.user.save()

        cls.fund1_pk = Fund.objects.create(name="First fund",
                                           cash_on_hand_cents=0).pk
        cls.fund2_pk = Fund.objects.create(name="Second fund",
                                           cash_on_hand_cents=0).pk

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self) -> None:
        """
        Clean up all posts after every test.
        :return:
        """
        Post.objects.all().delete()

    def validate_post(self, post_dict, post_obj, fund_pk):
        """
        Verify that JSON post representation is correct.
        :param post_dict: JSON dict representation of serialized post
        :param post_obj: Instance of post to compare post_dict to
        :param fund_pk: Primary key of Fund associated with post_obj
        :return:
        """
        self.assertEqual(post_dict['id'], post_obj.id)
        self.assertEqual(datetime.strptime(post_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                         post_obj.created_at)
        self.validate_fund(post_dict['fund'], fund_pk)
        self.assertEqual(post_dict['message'], post_obj.message)
        self.assertEqual(len(post_dict['videos']), 0)
        self.assertEqual(len(post_dict['articles']), 0)

    def validate_fund(self, fund_dict, fund_pk):
        """
        Verify that JSON fund representation is correct.
        :param fund_dict: JSON dict representation of serialized fund
        :param fund_pk: Primary key of Fund
        :return:
        """
        f = Fund.objects.get(pk=fund_pk)
        self.assertEqual(fund_dict['name'], f.name)
        self.assertEqual(fund_dict['id'], fund_pk)

    def test_one_post(self):
        """
        Verify that one post is gotten correctly.
        :return:
        """
        p = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                message='this is a message')

        response = self.client.get('/api/v1/feed/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json['posts']), 1)
        self.validate_post(json['posts'][0], p, self.fund1_pk)

    def test_no_posts(self):
        """
        Verify that no posts are returned.
        :return:
        """
        response = self.client.get('/api/v1/feed/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json['posts']), 0)

    def test_order_of_many_posts(self):
        """
        Verify order of posts are according to when they were created.
        :return:
        """
        p1 = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                 message='this is a message')
        p2 = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                 message='this is a message 2')
        p3 = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                 message='this is a message 3')

        response = self.client.get('/api/v1/feed/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json['posts']), 3)
        self.validate_post(json['posts'][0], p3, self.fund1_pk)
        self.validate_post(json['posts'][1], p2, self.fund1_pk)
        self.validate_post(json['posts'][2], p1, self.fund1_pk)

    def test_order_of_posts_from_different_funds(self):
        """
        Verify that order of posts hold when posts are from different funds.
        :return:
        """
        p1 = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                 message='this is a message')
        p2 = Post.objects.create(fund=Fund.objects.get(pk=self.fund2_pk),
                                 message='this is a message 2')
        p3 = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                 message='this is a message 3')

        response = self.client.get('/api/v1/feed/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json['posts']), 3)
        self.validate_post(json['posts'][0], p3, self.fund1_pk)
        self.validate_post(json['posts'][1], p2, self.fund2_pk)
        self.validate_post(json['posts'][2], p1, self.fund1_pk)

    def test_deleted_posts_do_not_show_up(self):
        """
        Make sure that posts marked as deleted are not retrieved.
        :return:
        """
        Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                            message='this is a message', is_deleted=True)
        p = Post.objects.create(fund=Fund.objects.get(pk=self.fund1_pk),
                                message='this is a message 2')

        response = self.client.get('/api/v1/feed/')
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json['posts']), 1)
        self.validate_post(json['posts'][0], p, self.fund1_pk)
