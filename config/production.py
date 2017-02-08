from config.settings import *
import dj_database_url

ALLOWED_HOSTS = ['farm.whillas.com', 'mindikatta.herokuapp.com']

# override databases, use Heroku's

DATABASES = {
    'default': dj_database_url.config()
}
