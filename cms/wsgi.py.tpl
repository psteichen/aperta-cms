"""
WSGI config for cms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

# set sys.path to the directory containing the django app
# else wsgi will not find the settings file below
sys.path.append('[FULL PATH OF DJANGO PROJECT CONTAINING FOLDER (one up)]')
sys.path.append('[FULL PATH OF DJANGO PROJECT]')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

application = get_wsgi_application()
