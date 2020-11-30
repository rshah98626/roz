#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from .fund import Fund


class Post(models.Model):
    """
    Similar to tweets, these objects represent a message the trader may have.
    """

    created_at = models.DateTimeField('When the post was created',
                                      auto_now_add=True)
    message = models.CharField('The content of the post', blank=True,
                               max_length=200)
    fund = models.ForeignKey(Fund, related_name='posts',
                             on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField('Determines if the post is not to'
                                     ' be shown', default=False)
