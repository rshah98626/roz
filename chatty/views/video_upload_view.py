#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

import time
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from chatty.models import Fund, Video


class AuthenticatedView(APIView):
    """
    A base view which mandates access to only authenticated users.
    """
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class VideoUploadView(AuthenticatedView):
    """
    View which uploads a video and associates it to a fund.
    """
    parser_classes = (FileUploadParser, )
    accepted_media_types = ['video/mp4', 'video/quicktime']

    def put(self, request, fund_id):
        """
        PUT a video and associated it with a fund.
        :param request:
        :param fund_id: A valid fund id to associate with the video.
        :return:
        """
        # validate parsing went correctly
        if 'file' not in request.data:
            raise ParseError("File unable to be parsed.")
        if request.content_type not in self.accepted_media_types:
            raise UnsupportedMediaType(media_type=request.content_type)

        # validate fund exists
        try:
            fund = Fund.objects.get(pk=fund_id)
        except Fund.DoesNotExist:
            return Response({'detail': 'Invalid fund id provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # formulate filename
        file = request.data['file']
        file_extension = 'mp4' if request.content_type == 'video/mp4' else 'mov'
        filename = f'{int(time.time())}_fund_{fund_id}_{file.name}.{file_extension}'

        # instantiate & save video object
        video = Video.objects.create(fund=fund)
        video.file.save(filename, file, save=True)
        return Response({'message': 'Video created', 'video_id': video.id, 'filename': filename},
                        status=status.HTTP_201_CREATED)
