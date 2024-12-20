from .base import *


INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]

MIDDLEWARE = [
    *MIDDLEWARE,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ALLOWED_HOSTS = [host for host in os.getenv("ALLOWED_HOSTS").split(",")]

INTERNAL_IPS = [
    "127.0.0.1",
]
