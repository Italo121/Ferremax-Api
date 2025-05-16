"""
ASGI config for ferremas_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferremas_api.settings')

application = get_asgi_application()

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django_eventstream.routing import router as eventstream_router

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferremas_api.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": URLRouter([
        *eventstream_router.urls
    ])
})