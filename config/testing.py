import dj_database_url

from config.settings import *

DATABASES = {
	# 'default': {
	# 	'ENGINE': 'django.db.backends.sqlite3',
	# 	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	# }
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'mindikatta_testing',
		'USER': 'alex',
		'PASSWORD': 'xela',
		'HOST': 'localhost',
		'PORT': '',
	}
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
