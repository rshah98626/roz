#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Article, Fund
from datetime import datetime, timezone


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(cash_on_hand_cents=0)
        fund.save()

        # init article
        cls.before_create = datetime.now(timezone.utc)
        cls.article_text = "This is a cool stock you should buy. It's called..."
        article = Article(
            text=cls.article_text,
            fund=fund
        )
        article.save()

    def test_field_labels(self):
        article = Article.objects.latest('id')
        self.assertEquals(article._meta.get_field('created_at').verbose_name, 'When the article was created')
        self.assertEquals(article._meta.get_field('fund').verbose_name, 'fund')
        self.assertEquals(article._meta.get_field('text').verbose_name, 'The long form content of the article')

    def test_text(self):
        self.assertEquals(Article.objects.latest('id').text, self.article_text)

    def test_fund(self):
        self.assertEquals(Article.objects.latest('id').fund, Fund.objects.latest('id'))

    def test_created_at(self):
        self.assertGreater(Article.objects.latest('id').created_at, self.before_create)
