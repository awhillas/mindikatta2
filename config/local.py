import dj_database_url

from config.settings import *

SITE_TITLE = "Mindikatta DEV"

# Setup for the docker-compose.yaml
DATABASES = {
    # 'default': {
    # 	'ENGINE': 'django.db.backends.sqlite3',
    # 	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mindikatta_local",
        "USER": "alex",
        "PASSWORD": "xela",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
