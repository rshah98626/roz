#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from ..models import Fund, Video
import time


class AuthenticatedView(APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class VideoView(AuthenticatedView):
    parser_classes = (FileUploadParser, )
    accepted_media_types = ['video/mp4', 'video/quicktime']

    def put(self, request, pk):
        # validate parsing went correctly
        if 'file' not in request.data:
            raise ParseError("File unable to be parsed.")
        if request.content_type not in self.accepted_media_types:
            raise UnsupportedMediaType(media_type=request.content_type)

        # validate fund exists
        try:
            fund = Fund.objects.get(pk=pk)
        except Fund.DoesNotExist:
            return Response({'detail': 'Invalid fund id provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # formulate filename
        file = request.data['file']
        file_extension = 'mp4' if request.content_type == 'video/mp4' else 'mov'
        filename = f'{int(time.time())}_fund_{pk}_{file.name}.{file_extension}'

        # instantiate & save video object
        video = Video.objects.create(fund=fund)
        video.file.save(filename, file, save=True)
        return Response({'message': 'Video created', 'video_id': video.id, 'filename': filename},
                        status=status.HTTP_201_CREATED)
