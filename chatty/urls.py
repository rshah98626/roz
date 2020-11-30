#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.urls import include, path
from chatty.views import VideoUploadView, FeedView

urlpatterns = [
    path('', include('users.urls')),
    path('fund/<int:fund_id>/video/upload/', VideoUploadView.as_view()),
    path('feed/', FeedView.as_view())
]
