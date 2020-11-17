#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Post, Fund, Article, Video
from datetime import datetime, timezone


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(name="First Fund", cash_on_hand_cents=0)
        fund.save()

        cls.before_create = datetime.now(timezone.utc)
        cls.post_message1 = "Here's my first post"
        cls.post_message2 = 'We\'re buying Tesla today guys! 2000 is a lucky number.'
        cls.article_message1 = "This is the first article I've written. I recommend you buy $ORNGE because it's going" \
                               " to do well during earnings."
        cls.video_message = "This is a video"

        # init posts
        post1 = Post(
            message=cls.post_message1,
            fund=fund
        )
        post1.save()

        post2 = Post(
            message=cls.post_message2,
            fund=fund
        )
        post2.save()

        post3 = Post(
            fund=fund,
            is_deleted=True
        )
        post3.save()

        # init article
        article1 = Article(
            text=cls.article_message1,
            post=post1
        )
        article1.save()

        # init video
        video1 = Video(
            post=post2,
            description=cls.video_message
        )
        video1.save()

    def test_field_labels(self):
        post = Post.objects.latest('id')
        self.assertEqual(post._meta.get_field('message').verbose_name,
                         'The content of the post')
        self.assertEqual(post._meta.get_field('created_at').verbose_name,
                         'When the post was created')
        self.assertEqual(post._meta.get_field('fund').verbose_name,
                         'fund')

    def test_message(self):
        posts = list(Post.objects.all())
        self.assertEqual(posts[0].message, self.post_message1)
        self.assertEqual(posts[1].message, self.post_message2)
        self.assertEqual(posts[2].message, '')

    def test_fund(self):
        only_fund = Fund.objects.latest('id')
        for p in list(Post.objects.all()):
            self.assertEqual(p.fund, only_fund)

    def test_created_at(self):
        posts = list(Post.objects.all())
        self.assertGreater(posts[0].created_at, self.before_create)
        self.assertGreater(posts[1].created_at, posts[0].created_at)
        self.assertGreater(posts[2].created_at, posts[1].created_at)

    def test_article(self):
        post = list(Post.objects.all())[0]
        self.assertEqual(len(post.articles.all()), 1)
        self.assertEqual(post.articles.first().text, self.article_message1)

    def test_no_articles(self):
        posts = list(Post.objects.all())
        self.assertEqual(len(posts[1].articles.all()), 0)
        self.assertEqual(len(posts[2].articles.all()), 0)

    def test_video(self):
        post = list(Post.objects.all())[1]
        self.assertEqual(len(post.videos.all()), 1)
        self.assertEqual(post.videos.first().description, self.video_message)

    def test_no_videos(self):
        posts = list(Post.objects.all())
        self.assertEqual(len(posts[0].videos.all()), 0)
        self.assertEqual(len(posts[2].videos.all()), 0)

    def test_is_deleted(self):
        post = Post.objects.latest('id')
        self.assertTrue(post.is_deleted)
