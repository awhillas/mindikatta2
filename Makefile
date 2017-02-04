go:
	python ./manage.py runserver_plus

deps:
	pip-compile --output-file requirements.txt requirements.in
	pip-sync requirements.txt
