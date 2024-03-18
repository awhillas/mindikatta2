import dj_database_url

from config.settings import *

ALLOWED_HOSTS = [
    "farm.whillas.com",
]

# override databases, use Heroku's

DATABASES = {"default": dj_database_url.config()}


# Email setup
# see: https://anymail.readthedocs.io/en/stable/installation/

# INSTALLED_APPS += ["anymail"]

# EMAIL_BACKEND = "anymail.backends.sendgrid.SendGridBackend"

# ANYMAIL = {
#     "SENDGRID_API_KEY": "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"
# }

# DEFAULT_FROM_EMAIL = "Mindikatta Webmaster <whillas@gmail.com>"
