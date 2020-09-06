#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Post, Fund
from datetime import datetime, timezone


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(cash_on_hand_cents=0)
        fund.save()

        cls.before_create = datetime.now(timezone.utc)
        cls.message = "Here's my first post"

        post = Post(
            message=cls.message,
            fund=fund
        )
        post.save()

    def test_field_labels(self):
        post = Post.objects.latest('id')
        self.assertEquals(post._meta.get_field('message').verbose_name, 'The content of the post')
        self.assertEquals(post._meta.get_field('created_at').verbose_name, 'When the post was created')
        self.assertEquals(post._meta.get_field('fund').verbose_name, 'fund')

    def test_message(self):
        self.assertEquals(Post.objects.latest('id').message, self.message)

    def test_fund(self):
        self.assertEquals(Post.objects.latest('id').fund, Fund.objects.latest('id'))