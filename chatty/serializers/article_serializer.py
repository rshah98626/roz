#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from chatty.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    This class allows for an Article model to be represented in JSON.
    """
    class Meta:
        model = Article
        fields = ['text', 'created_at', 'id']
