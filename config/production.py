from config.settings import *
import dj_database_url

ALLOWED_HOSTS = ['farm.whillas.com', 'mindikatta.herokuapp.com']

# override databases, use Heroku's

DATABASES = {
    'default': dj_database_url.config()
}


# Email setup
# see: https://anymail.readthedocs.io/en/stable/installation/

INSTALLED_APPS += ["anymail"]

# EMAIL_BACKEND = "anymail.backends.sendgrid.SendGridBackend"
EMAIL_BACKEND = "anymail.backends.sendgrid_v2.EmailBackend"  # legacy coz it works

ANYMAIL = {
    'SENDGRID_API_KEY': os.getenv('SENDGRID_API_KEY'),
    'SENDGRID_USERNAME': os.getenv('SENDGRID_USERNAME'),
    'SENDGRID_PASSWORD': os.getenv('SENDGRID_PASSWORD'),
}

DEFAULT_FROM_EMAIL = 'Mindikatta Webmaster <whillas@gmail.com>'
