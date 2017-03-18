go:
	python ./manage.py runserver_plus

deps:
	pip-compile --output-file requirements.txt ./config/requirements.in
	pip-sync requirements.txt

models:
	python ./manage.py makemigrations
	python ./manage.py migrate

test:
	python ./manage.py test --traceback --failfast -v 1 --settings=config.testing

deploy:
	git push heroku master

me:
	python manage.py createsuperuser --username alex --email whillas@gmail.com

logs:
	heroku logs --app mindikatta

db-start:
	# Start local Postgres DB (we're using sqlite for now)
	pg_ctl -D /usr/local/var/postgres9.5 -l ~/postgres9.5.log start

db-copy:
	# Copy the live DB
	dropdb mindikatta_local
	heroku pg:pull DATABASE_URL mindikatta_local --app mindikatta

db-backup:
	heroku pg:backups:capture --app mindikatta
	heroku pg:backups:download --app mindikatta

db-restore:
	pg_restore --verbose --clean --create --no-acl --no-owner -h localhost -U alex -d mindikatta_local latest.dump
