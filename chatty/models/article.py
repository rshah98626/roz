#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from chatty.models import Post


class Article(models.Model):
    """
    This is an object that represents an article which correlates to a fund.
    """

    created_at = models.DateTimeField(
        'When the article was created', auto_now_add=True)
    text = models.TextField('The long form content of the article')
    post = models.ForeignKey(Post, related_name='articles',
                             on_delete=models.SET_NULL, null=True)
