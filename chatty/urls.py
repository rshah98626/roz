#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.urls import include, path
from .views import VideoView

urlpatterns = [
    path('', include('users.urls')),
    path('fund/<int:pk>/video/upload/', VideoView.as_view())
]
