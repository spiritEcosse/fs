"""
WSGI config for fs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from fs.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fs.settings")

# Activate your virtual env
activate_env = os.path.expanduser(os.path.join(BASE_DIR, "ENV/bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))

application = get_wsgi_application()
