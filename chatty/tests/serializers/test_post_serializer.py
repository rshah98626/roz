#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from datetime import datetime, timezone
from io import BytesIO
from unittest.mock import patch

from django.test import TestCase

from chatty.models import Fund, Post, Article, Video
from chatty.serializers import PostSerializer


class PostSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # constants
        cls.fund_name = 'Fundy'

        cls.post1_message = 'first post'
        cls.post2_message = 'second post'
        cls.post3_message = 'third post'
        cls.post4_message = 'fourth post'
        cls.post5_message = 'fifth post'

        cls.video1_description = 'video1 description'
        cls.video2_description = 'video2 description'
        cls.video3_description = 'video3 description'
        cls.video4_description = 'video4 description'

        cls.article1_text = 'article 1 text'
        cls.article2_text = 'article 2 text'
        cls.article3_text = 'article 3 text'
        cls.article4_text = 'article 4 text'

        # instantiate test data
        fund = Fund.objects.create(cash_on_hand_cents=0, name=cls.fund_name)
        post1 = Post.objects.create(fund=fund, message=cls.post1_message)
        cls.post1_id = post1.id

        post2 = Post.objects.create(fund=fund, message=cls.post2_message)
        cls.post2_id = post2.id
        video1 = Video.objects.create(post=post2, description=cls.video1_description)
        cls.video1_id = video1.id
        Article.objects.create(post=post2, text=cls.article1_text)

        post3 = Post.objects.create(fund=fund, message=cls.post3_message)
        cls.post3_id = post3.id
        video2 = Video.objects.create(post=post3, description=cls.video2_description)
        cls.video2_id = video2.id

        post4 = Post.objects.create(fund=fund, message=cls.post4_message)
        cls.post4_id = post4.id
        Article.objects.create(post=post4, text=cls.article2_text)

        post5 = Post.objects.create(fund=fund, message=cls.post5_message)
        cls.post5_id = post5.id
        video3 = Video.objects.create(post=post5, description=cls.video3_description)
        cls.video3_id = video3.id
        Article.objects.create(post=post5, text=cls.article3_text)
        video4 = Video.objects.create(post=post5, description=cls.video4_description)
        cls.video4_id = video4.id
        Article.objects.create(post=post5, text=cls.article4_text)

    def test_post_deserialization(self):
        serializer = PostSerializer(data={
            'message': 'This is a post',
            'fund': {
                'name': f'{self.fund_name}s'
            }
        })
        self.assertTrue(serializer.is_valid())

    def test_no_videos_no_articles(self):
        p = Post.objects.get(pk=self.post1_id)
        serialized_data = PostSerializer(p).data

        self.assertEqual(serialized_data['message'], self.post1_message)
        self.assertEqual(serialized_data['fund']['name'], self.fund_name)
        self.assertEqual(serialized_data['id'], self.post1_id)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.now(timezone.utc)
        )

    @patch('storages.backends.s3boto3.S3Boto3Storage.url')
    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_one_video_one_article(self, mock_filename, url_name):
        mock_filename.return_value = 'filename'
        url_name.return_value = 'localhost'
        p = Post.objects.get(pk=self.post2_id)
        v = Video.objects.get(pk=self.video1_id)
        v.file.save('filename', BytesIO(b'file'), save=True)
        serialized_data = PostSerializer(p).data

        self.assertEqual(serialized_data['message'], self.post2_message)
        self.assertEqual(serialized_data['fund']['name'], self.fund_name)
        self.assertEqual(serialized_data['id'], self.post2_id)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.now(timezone.utc)
        )

        # verify video serialization
        self.assertEqual(serialized_data['videos'][0]['url'], 'localhost')
        self.assertEqual(serialized_data['videos'][0]['id'], self.video1_id)
        self.assertEqual(serialized_data['videos'][0]['description'], self.video1_description)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['videos'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )

        # verify post serialization
        self.assertEqual(serialized_data['articles'][0]['text'], self.article1_text)
        self.assertLess(
            datetime.strptime(serialized_data['videos'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['articles'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )

    @patch('storages.backends.s3boto3.S3Boto3Storage.url')
    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_one_video(self, mock_filename, url_name):
        mock_filename.return_value = 'filename'
        url_name.return_value = 'localhost'
        p = Post.objects.get(pk=self.post3_id)
        v = Video.objects.get(pk=self.video2_id)
        v.file.save('filename', BytesIO(b'file'), save=True)
        serialized_data = PostSerializer(p).data

        self.assertEqual(serialized_data['message'], self.post3_message)
        self.assertEqual(serialized_data['fund']['name'], self.fund_name)
        self.assertEqual(serialized_data['id'], self.post3_id)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.now(timezone.utc)
        )
        self.assertEqual(serialized_data['videos'][0]['url'], 'localhost')
        self.assertEqual(serialized_data['videos'][0]['id'], self.video2_id)
        self.assertEqual(serialized_data['videos'][0]['description'], self.video2_description)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['videos'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )

    def test_one_article(self):
        p = Post.objects.get(pk=self.post4_id)
        serialized_data = PostSerializer(p).data

        self.assertEqual(serialized_data['message'], self.post4_message)
        self.assertEqual(serialized_data['fund']['name'], self.fund_name)
        self.assertEqual(serialized_data['id'], self.post4_id)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.now(timezone.utc)
        )

        # verify post serialization
        self.assertEqual(serialized_data['articles'][0]['text'], self.article2_text)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['articles'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )

    @patch('storages.backends.s3boto3.S3Boto3Storage.url')
    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_multiple_assets(self, mock_filename, url_name):
        mock_filename.return_value = 'filename'
        url_name.return_value = 'localhost'
        p = Post.objects.get(pk=self.post5_id)
        v1, v2 = Video.objects.get(pk=self.video3_id), Video.objects.get(pk=self.video4_id)
        v1.file.save('filename', BytesIO(b'file'), save=True)
        v2.file.save('filename', BytesIO(b'file'), save=True)
        serialized_data = PostSerializer(p).data

        self.assertEqual(serialized_data['message'], self.post5_message)
        self.assertEqual(serialized_data['fund']['name'], self.fund_name)
        self.assertEqual(serialized_data['id'], self.post5_id)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.now(timezone.utc)
        )

        # verify video serialization
        self.assertEqual(serialized_data['videos'][1]['url'], 'localhost')
        self.assertEqual(serialized_data['videos'][1]['id'], self.video3_id)
        self.assertEqual(serialized_data['videos'][1]['description'], self.video3_description)
        self.assertLess(
            datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['videos'][1]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )
        self.assertEqual(serialized_data['videos'][0]['url'], 'localhost')
        self.assertEqual(serialized_data['videos'][0]['id'], self.video4_id)
        self.assertEqual(serialized_data['videos'][0]['description'], self.video4_description)
        self.assertLess(
            datetime.strptime(serialized_data['articles'][1]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['videos'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )

        # verify post serialization
        self.assertEqual(serialized_data['articles'][1]['text'], self.article3_text)
        self.assertLess(
            datetime.strptime(serialized_data['videos'][1]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['articles'][1]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )
        self.assertEqual(serialized_data['articles'][0]['text'], self.article4_text)
        self.assertLess(
            datetime.strptime(serialized_data['videos'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            datetime.strptime(serialized_data['articles'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        )
