#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from chatty.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    This class specifies how videos should be represented as JSON.
    """
    url = serializers.CharField(source='get_url', read_only=True)

    class Meta:
        model = Video
        fields = ['description', 'created_at', 'url']
