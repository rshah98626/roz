#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),
]
