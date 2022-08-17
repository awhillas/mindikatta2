# Mindikatta v.2

Nut tracking (Django) web app.

## Setup

### Heroku

1. [Setup Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

    curl https://cli-assets.heroku.com/install.sh | sh

to verify

    heroku --version

then login

    heroku login

[Setup postgresql locally](https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04) for dumping and running in development. To get the latest version setup the `apt` certificates

    sudo apt install wget ca-certificates
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

then install

    sudo apt update
    apt install postgresql postgresql-contrib

then check the status of the service

    service postgresql status

if its `down`

    12/main (port 5432): online
    14/main (port 5433): down

start it with, where `14` here is the version of the server

    sudo pg_ctlcluster 14 main start

Your going to have to setup a user and a corresponding DB

    sudo -u postgres createuser --superuser $USER
    sudo -u postgres createdb $USER
    touch ~/.psql_history

then typing `psql` should get you into the postgres shell (`\q` to exit). Then dump the online DB to local

    heroku pg:pull DATABASE_URL mindikatta_local --app mindikatta

### Local python environment

    python3.  -m venv --prompt mindikatta __venv__
    pip install

## Database changes

Make changes in the `mindikatta/harvest/models.py` file then

    make models
    make tests

to update the live DB on heroku you need to ssh into the live instance

    heroku run bash

and then run:

    python manage.py migrate

## Deployment

Deployment is to Heroku which monitors the master branch of the github repo that it has created

    make deploy

## Feature Requests

- "would be good to be able to go into each type of nut to see the individual entries"
- Graph current year vs historical average
- Linear regression

## Bugs

- Timezone differences between DB and Pandas