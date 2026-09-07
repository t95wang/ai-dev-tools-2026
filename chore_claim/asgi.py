"""ASGI config for the Chore Claim System."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chore_claim.settings")

application = get_asgi_application()
