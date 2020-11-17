#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Article, Fund, Post
from datetime import datetime, timezone


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(name="First fund", cash_on_hand_cents=0)
        fund.save()
        post = Post(fund=fund)
        post.save()

        # init article
        cls.before_create = datetime.now(timezone.utc)
        cls.article_text = "This is a cool stock you should buy. It's called..."
        article = Article(
            text=cls.article_text,
            post=post
        )
        article.save()

    def test_field_labels(self):
        article = Article.objects.latest('id')
        self.assertEqual(article._meta.get_field('created_at').verbose_name,
                         'When the article was created')
        self.assertEqual(article._meta.get_field('post').verbose_name, 'post')
        self.assertEqual(article._meta.get_field('text').verbose_name,
                         'The long form content of the article')

    def test_text(self):
        self.assertEqual(Article.objects.latest('id').text,
                         self.article_text)

    def test_post(self):
        self.assertEqual(Article.objects.latest('id').post,
                         Post.objects.latest('id'))

    def test_created_at(self):
        self.assertGreater(Article.objects.latest('id').created_at,
                           self.before_create)
