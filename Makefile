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

db-refresh:
	dropdb mindikatta_local
	createdb mindikatta_local
	python ./manage.py migrate
	sed 's/`//g' mindikatta.sql | psql mindikatta_local

db-dump:
	pg_dump mindikatta_local | gzip > mindikatta_local.dump.gz

db-restore:
	gunzip -c mindikatta_local.dump.gz | psql mindikatta_local

db-push:
	# Local backup to heroku. DESTORYS THE LIVE VERSION!!
	heroku pg:reset --app mindikatta
	heroku run python manage.py migrate
	heroku pg:push mindikatta_local DATABASE --app mindikatta
