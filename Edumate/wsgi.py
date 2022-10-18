"""
WSGI config for Edumate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/my-project-dir')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Edumate.settings')

application = get_wsgi_application()
