#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from datetime import datetime, timezone
from chatty.serializers import VideoSerializer
from chatty.models import Video, Fund, Post
from io import BytesIO
from unittest.mock import patch


class VideoSerializerTest(TestCase):
    def test_video_deserialization(self):
        serializer = VideoSerializer(data={
            'description': 'cool video'
        })
        self.assertTrue(serializer.is_valid())

    @patch('storages.backends.s3boto3.S3Boto3Storage.url')
    def test_video_serialization(self, url_name):
        url_name.return_value = "localhost"
        description = 'cool video'

        f = Fund.objects.create(cash_on_hand_cents=0, name='First Fund')
        p = Post.objects.create(fund=f)
        v = Video.objects.create(post=p, description=description)
        v.file.save('filename', BytesIO(b'file'), save=True)

        serialized_data = VideoSerializer(v).data

        self.assertEqual(serialized_data['description'], description)
        self.assertLess(datetime.strptime(serialized_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                        datetime.now(timezone.utc))
        self.assertEqual(serialized_data['url'], 'localhost')
        self.assertEqual(serialized_data['id'], v.id)
