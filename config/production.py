from config.settings import *
import dj_database_url


# override databases, use Heroku's

DATABASES = {
    'default': dj_database_url.config()
}
