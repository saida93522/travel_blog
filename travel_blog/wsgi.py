"""
WSGI config for travel_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

This is an entry point for Blog site which is used by the web servers to serve the project created.
web server gateway interface(actual server)

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_blog.settings')

application = get_wsgi_application()
