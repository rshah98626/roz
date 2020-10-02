#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from .fund import Fund
from roz.custom_storage import VideoStorage


class Video(models.Model):
    """
    This is an object which represents a video which correlates to a specific fund.
    """

    created_at = models.DateTimeField('When the video was created', auto_now_add=True)
    file = models.FileField('The video file instance', storage=VideoStorage())
    description = models.TextField('A description of what the video is about', null=True)
    fund = models.ForeignKey(Fund, related_name='videos', on_delete=models.SET_NULL, null=True)
