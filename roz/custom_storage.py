#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class VideoStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'videos'
