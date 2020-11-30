#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from roz.custom_storage import VideoStorage
from chatty.models import Post


class Video(models.Model):
    """
    This is an object which represents a video which correlates to a specific fund.
    """

    created_at = models.DateTimeField(
        'When the video was created', auto_now_add=True)
    file = models.FileField('The video file instance', storage=VideoStorage())
    description = models.TextField(
        'A description of what the video is about', null=True)
    post = models.ForeignKey(Post, related_name='videos',
                             on_delete=models.SET_NULL, null=True)

    def get_url(self):
        """
        Get the URL of the file so that it can be added to the serializer.
        :return:
        """
        return self.file.url
