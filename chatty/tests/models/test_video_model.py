#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Video, Fund
from datetime import datetime, timezone
from io import BytesIO
from unittest.mock import patch


class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(cash_on_hand_cents=0)
        fund.save()

        # init video 1
        cls.before_create1 = datetime.now(timezone.utc)
        video1 = Video(
            fund=fund
        )
        video1.save()

        # init video 2
        cls.before_create2 = datetime.now(timezone.utc)
        cls.video_description2 = "This is a description"
        video2 = Video(
            fund=fund,
            description=cls.video_description2
        )
        video2.save()

    def test_field_labels(self):
        video = Video.objects.latest('id')
        self.assertEqual(video._meta.get_field(
            'description').verbose_name, 'A description of what the video is about')
        self.assertEqual(video._meta.get_field(
            'created_at').verbose_name, 'When the video was created')
        self.assertEqual(video._meta.get_field('fund').verbose_name, 'fund')

    def test_description(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertIsNone(video1.description)
        self.assertEqual(video2.description, self.video_description2)

    def test_fund(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertEqual(video1.fund, Fund.objects.latest('id'))
        self.assertEqual(video2.fund, Fund.objects.latest('id'))

    def test_created_at(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertGreater(video1.created_at, self.before_create1)
        self.assertGreater(video2.created_at, self.before_create2)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_file_field(self, mock_filename):
        filename = 'file_name'
        mock_filename.return_value = filename
        v = Video.objects.create(fund=Fund.objects.latest('id'))
        v.file.save(filename, BytesIO(b'file'), save=True)

        video = Video.objects.latest('id')
        self.assertEqual(video.file.name, filename)

    @patch('storages.backends.s3boto3.S3Boto3Storage.url')
    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_file_url(self, mock_filename, mock_file_url):
        ret_url = 'hi.com/test.mov'
        mock_filename.return_value = 'test.mov'
        mock_file_url.return_value = ret_url
        v = Video.objects.create(fund=Fund.objects.latest('id'))
        v.file.save('name', BytesIO(b'file'), save=True)

        video = Video.objects.latest('id')
        self.assertEqual(video.get_url(), ret_url)
