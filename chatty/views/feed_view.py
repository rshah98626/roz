#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework.response import Response
from rest_framework import status
from roz.inheritable_views import AuthenticatedView
from chatty.models import Post
from chatty.serializers import PostSerializer


class FeedView(AuthenticatedView):
    """
    View which provides a feed of Posts associated all Funds.
    """

    def get(self, request):
        """
        GET a list of Posts associated with all funds.
        :return:
        """
        posts = Post.objects.all().filter(is_deleted=False)\
                    .order_by('-created_at')
        return Response({'posts': PostSerializer(posts, many=True).data},
                        status=status.HTTP_200_OK)
