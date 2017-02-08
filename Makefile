go:
	python ./manage.py runserver_plus

deps:
	pip-compile --output-file requirements.txt ./config/requirements.in
	pip-sync requirements.txt

migrate:
	python ./manage.py makemigrations
	python ./manage.py migrate

test:
	python ./manage.py test --traceback --failfast -v 1

deploy:
	git push heroku master

logs:
	heroku logs --app mindikatta
