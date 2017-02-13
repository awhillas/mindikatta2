from config.settings import *
import dj_database_url


DATABASES = {
	# 'default': {
	# 	'ENGINE': 'django.db.backends.sqlite3',
	# 	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	# }
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'mindikatta_local',
			'USER': 'alex',
			'PASSWORD': '',
			'HOST': 'localhost',
			'PORT': '',
		}
}
