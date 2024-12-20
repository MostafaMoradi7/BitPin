from .base import *

ALLOWED_HOSTS = [host for host in os.getenv("ALLOWED_HOSTS").split(",")]
