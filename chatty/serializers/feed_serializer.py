#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from chatty.models import Fund
from chatty.serializers import VideoSerializer


class FeedSerializer(serializers.ModelSerializer):
    """
    This class describes how to serialize a Fund object
    """
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Fund
        fields = ['name', 'videos']
