#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Video, Fund
from datetime import datetime, timezone


class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(cash_on_hand_cents=0)
        fund.save()

        # init video 1
        cls.before_create1 = datetime.now(timezone.utc)
        cls.video_filename1 = "happy.mp4"
        video1 = Video(
            file_name=cls.video_filename1,
            fund=fund
        )
        video1.save()

        # init video 2
        cls.before_create2 = datetime.now(timezone.utc)
        cls.video_filename2 = "hi.mov"
        cls.video_description2 = "This is a description"
        video2 = Video(
            file_name=cls.video_filename2,
            fund=fund,
            description=cls.video_description2
        )
        video2.save()

    def test_field_labels(self):
        video = Video.objects.latest('id')
        self.assertEquals(video._meta.get_field('description').verbose_name, 'A description of what the video is about')
        self.assertEquals(video._meta.get_field('created_at').verbose_name, 'When the video was created')
        self.assertEquals(video._meta.get_field('fund').verbose_name, 'fund')
        self.assertEquals(video._meta.get_field('file_name').verbose_name, 'The filename of where the video can be'
                                                                           ' retrieved from')

    def test_description(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertIsNone(video1.description)
        self.assertEquals(video2.description, self.video_description2)

    def test_fund(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertEquals(video1.fund, Fund.objects.latest('id'))
        self.assertEquals(video2.fund, Fund.objects.latest('id'))

    def test_file_name(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertEquals(video1.file_name, self.video_filename1)
        self.assertEquals(video2.file_name, self.video_filename2)

    def test_created_at(self):
        videos = Video.objects.all()
        video1, video2 = videos.first(), videos.last()
        self.assertGreater(video1.created_at, self.before_create1)
        self.assertGreater(video2.created_at, self.before_create2)
