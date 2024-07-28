import os

import dj_database_url
from config.settings import *

print("Using production settings")

ALLOWED_HOSTS = [
    "*",
]

# override databases, use Heroku's

DATABASES = {"default": dj_database_url.config()}

STATIC_ROOT = os.getenv("STATIC_ROOT", "/data/static")

# Email setup
# see: https://anymail.readthedocs.io/en/stable/installation/

# INSTALLED_APPS += ["anymail"]

# EMAIL_BACKEND = "anymail.backends.sendgrid.SendGridBackend"

# ANYMAIL = {
#     "SENDGRID_API_KEY": "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"
# }

# DEFAULT_FROM_EMAIL = "Mindikatta Webmaster <whillas@gmail.com>"
