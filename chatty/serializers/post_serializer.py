#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from chatty.models import Post
from chatty.serializers import ArticleSerializer, VideoSerializer, FundSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    This class describes how to serialize a Post object
    """
    videos = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    fund = FundSerializer(many=False)

    class Meta:
        model = Post
        fields = ['id', 'created_at', 'message',
                  'fund', 'videos', 'articles']

    def get_videos(self, instance):
        videos = instance.videos.all().order_by('-created_at')
        return VideoSerializer(videos, many=True).data

    def get_articles(self, instance):
        articles = instance.articles.all().order_by('-created_at')
        return ArticleSerializer(articles, many=True).data
