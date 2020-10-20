#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from io import BytesIO
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase

from chatty.models import Fund, Video
from chatty.views import VideoView
from users.models import Account


class VideoUploadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'hello'
        cls.password = 'hellotwice'

        cls.user = Account(
            email="hi@cmail.com",
            username=cls.username,
            first_name="Ray",
            last_name="Pay"
        )
        cls.user.set_password(cls.password)
        cls.user.save()

        fund = Fund(cash_on_hand_cents=100)
        fund.save()

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.testable_view = VideoView.as_view()
        self.client.force_authenticate(user=self.user)
        self.filename = "firstVideo"

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_video_is_uploaded(self, mock_save):
        # specify mocked return value, which in this case is the file name
        mock_save.return_value = 'filename'

        # set up request
        data = {'file': BytesIO(b'my_video_file')}
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}

        # make request
        response = self.client.put('/api/v1/fund/1/video/upload/', data=data,
                                   content_type='video/mp4', **headers)
        json = response.json()

        latest_video = Video.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(latest_video)
        self.assertEqual(json['message'], 'Video created')
        self.assertEqual(json['video_id'], latest_video.id)
        self.assertTrue(f'_fund_{latest_video.id}_{self.filename}.mp4' in json['filename'])
        self.assertEqual(latest_video.file.name, 'filename')
        mock_save.assert_called_once()
