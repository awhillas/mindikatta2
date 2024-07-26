 .PHONY: setup requirements go me update

DB_USER=alex
DOCKER_IMAGE=cpill/mindikatta

include .env

bootstrap:
	# Run me frist on a new setup
	pip install uv pip-tools setuptools wheel
	uv pip install -r requirements.txt

###### Database ######

db:
	docker-compose up -d

db_restore:
	docker exec -i mindikatta-db-1 pg_restore --verbose --clean --no-acl --no-owner -U postgres -d mindikatta_local < ../latest.dump


db_setup:
	# after starting the db
	createdb -h localhost -U $(DB_USER) -W mindikatta_local
	pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $(DB_USER) -d mindikatta_local ../latest.dump

db-start:
	# Start local Postgres DB (we're using sqlite for now)
	sudo pg_ctlcluster 14 main start

db-copy:
	# Copy the live DB
	dropdb mindikatta_local
	# TODO: replace this with 1. pg_dump of latest, 2. run local docker image, 3. restore from latest dump
	# heroku pg:pull DATABASE_URL mindikatta_local --app mindikatta

db-backup:
	pg_dump $(DATABASE_URL) > ../data/$(shell date '+%Y-%m-%d')_mindikatta_dump.sql

db-restore:
	pg_restore --verbose --clean --create --no-acl --no-owner -h localhost -U alex -d mindikatta_local latest.dump

###### Django ######

models:
	python ./manage.py makemigrations
	python ./manage.py migrate

test:
	python ./manage.py test --traceback --failfast -v 1

tests:
	python ./manage.py test --traceback -v 1

me:
	./manage.py createsuperuser --username alex --email whillas@gmail.com --settings=config.local
	./manage.py changepassword alex

go:
	# python ./manage.py runserver_plus
	python ./manage.py runserver

requrements:
	uv pip compile requirements/base.in --output-file requirements.txt
	uv pip compile requirements/dev.in --output-file requirements-dev.txt

update: requrements
	uv pip install -r requirements-dev.txt

###### Docker ######

image:
	# Bulid the docker image for the lambda functions
	docker build -t $(DOCKER_IMAGE):latest -t $(DOCKER_IMAGE):$(shell date '+%Y-%m-%d-%H-%M') .

push:
	# Push image to docker hub
	docker login --username=cpill --password $(shell cat .dockerhub)
	docker push $(DOCKER_IMAGE) --all-tags

go-local:
	# Run the dcker image locally
	docker run -p 3000:3000 -e DATABASE_URL=${DATABASE_URL} mindikatta:latest
