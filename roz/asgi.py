"""
ASGI config for roz project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roz.settings')

application = get_asgi_application()
