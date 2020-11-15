#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.urls import include, path
from .views import VideoUploadView

urlpatterns = [
    path('', include('users.urls')),
    path('fund/<int:fund_id>/video/upload/', VideoUploadView.as_view())
]
