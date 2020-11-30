#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from datetime import datetime, timezone
from django.test import TestCase
from chatty.serializers import ArticleSerializer
from chatty.models import Fund, Post, Article


class ArticleSerializerTest(TestCase):
    def test_article_deserialization(self):
        serializer = ArticleSerializer(data={
            'text': 'this is a test'
        })
        self.assertTrue(serializer.is_valid())

    def test_article_serialization(self):
        article_text = 'Hi mate'
        f = Fund.objects.create(cash_on_hand_cents=0, name='First fund')
        p = Post.objects.create(fund=f)
        a = Article.objects.create(post=p, text=article_text)

        serialized_data = ArticleSerializer(a).data

        self.assertEqual(serialized_data['text'], article_text)
        self.assertEqual(serialized_data['id'], a.id)
        self.assertLess(datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                        datetime.now(timezone.utc))
