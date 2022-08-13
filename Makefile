 .PHONY: setup requirements go me update

setup: me
	createdb mindikatta_local
	pip install pip-tools setuptools wheel
	pip install -r requirements.txt

me:
	python manage.py createsuperuser --username alex --email whillas@gmail.com  --settings=config.local

go:
	# python ./manage.py runserver_plus
	python ./manage.py runserver

requrements:
	pip-compile requirements/base.in --output-file requirements.txt
	pip-compile requirements/dev.in --output-file requirements-dev.txt

update: requrements
	pip install -r requirements-dev.txt

models:
	python ./manage.py makemigrations
	python ./manage.py migrate

test:
	python ./manage.py test --traceback --failfast -v 1

tests:
	python ./manage.py test --traceback -v 1

deploy:
	git push heroku master

logs:
	heroku logs --app mindikatta

db-start:
	# Start local Postgres DB (we're using sqlite for now)
	sudo pg_ctlcluster 14 main start

db-copy:
	# Copy the live DB
	dropdb mindikatta_local
	heroku pg:pull DATABASE_URL mindikatta_local --app mindikatta

db-backup:
	heroku pg:backups:capture --app mindikatta
	heroku pg:backups:download --app mindikatta

db-restore:
	pg_restore --verbose --clean --create --no-acl --no-owner -h localhost -U alex -d mindikatta_local latest.dump
