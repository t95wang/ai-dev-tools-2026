"""WSGI config for the Chore Claim System."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chore_claim.settings")

application = get_wsgi_application()
