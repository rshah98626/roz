#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from io import BytesIO
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from chatty.models import Fund, Video, Post
from chatty.views import VideoUploadView
from users.models import Account


class VideoUploadTest(APITestCase):
    """
    This class tests the video upload endpoint.
    """
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

        fund = Fund(name="First fund", cash_on_hand_cents=100)
        fund.save()
        cls.fund_pk = fund.pk

    def setUp(self):
        self.client = APIClient()
        self.testable_view = VideoUploadView.as_view()
        self.client.force_authenticate(user=self.user)
        self.filename = "firstVideo"

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_mp4_video_is_uploaded(self, mock_save):
        """
        Check to make sure that an mp4 can be uploaded.
        :param mock_save: Mock object returned by the storages backend.
        :return:
        """
        # specify mocked return value, which in this case is the file name
        mock_save.return_value = 'filename'

        # set up request
        data = BytesIO(b'my_video_file')
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}

        # make request
        response = self.client.put(f'/api/v1/fund/{self.fund_pk}/video/upload/', data=data,
                                   content_type='video/mp4', **headers)
        json = response.json()

        latest_video = Video.objects.latest('id')
        latest_post = Post.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(latest_video)
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.videos.first(), latest_video)
        self.assertEqual(json['message'], 'Video created')
        self.assertEqual(json['video_id'], latest_video.id)
        self.assertTrue(f'_fund_{self.fund_pk}_{self.filename}.mp4' in json['filename'])
        self.assertEqual(latest_video.file.name, 'filename')
        mock_save.assert_called_once()

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_quicktime_video_is_uploaded(self, mock_save):
        """
        Check to make sure quicktime video can be uploaded.
        :param mock_save: Mock object returned by the storages backend.
        :return:
        """
        mock_save.return_value = 'filename'

        data = BytesIO(b'my_video_file')
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}

        response = self.client.put(f'/api/v1/fund/{self.fund_pk}/video/upload/', data=data,
                                   content_type='video/quicktime', **headers)
        json = response.json()

        latest_video = Video.objects.latest('id')
        latest_post = Post.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(latest_video)
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.videos.first(), latest_video)
        self.assertEqual(json['message'], 'Video created')
        self.assertEqual(json['video_id'], latest_video.id)
        self.assertTrue(f'_fund_{self.fund_pk}_{self.filename}.mov' in json['filename'])
        self.assertEqual(latest_video.file.name, 'filename')
        mock_save.assert_called_once()

    def test_no_file_is_provided(self):
        """
        If a file is not given, make sure an error is returned.
        :return:
        """
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}
        response = self.client.put(f'/api/v1/fund/{self.fund_pk}/video/upload/', data=None,
                                   content_type='video/mp4', **headers)
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json['detail'], 'File unable to be parsed.')

    def test_no_filename_is_provided(self):
        """
        Verify that file can't be uploaded if a file name isn't provided.
        :return:
        """
        data = BytesIO(b'video_file')
        response = self.client.put(f'/api/v1/fund/{self.fund_pk}/video/upload/', data=data,
                                   content_type='video/mp4')
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json['detail'], 'Missing filename. Request should include a '
                                         'Content-Disposition header with a filename parameter.')

    def test_not_accepted_video_content_type(self):
        """
        If a file isn't a quicktime or mp4, make sure the video cannot be uploaded.
        :return:
        """
        unknown_content_type = 'video/x-flv'
        data = BytesIO(b'my_video_file')
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}

        response = self.client.put(f'/api/v1/fund/{self.fund_pk}/video/upload/', data=data,
                                   content_type=unknown_content_type, **headers)
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(json['detail'], f'Unsupported media type "{unknown_content_type}" in '
                                         f'request.')

    def test_fund_not_valid(self):
        """
        If a fund id is invalid, reject the upload request.
        :return:
        """
        data = BytesIO(b'my_video_file')
        headers = {'HTTP_CONTENT_DISPOSITION': f'attachment; filename={self.filename}'}

        response = self.client.put('/api/v1/fund/12398712398172391287319/video/upload/', data=data,
                                   content_type='video/mp4', **headers)
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json['detail'], 'Invalid fund id provided.')
