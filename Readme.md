# Mindikatta v.3

Nut tracking (Django) web app.

This is a Django app that is deployed on a Raspberry Pi.

## TODO

- [ ] Figureout some sort of backup system for DB


## Setup

### Local python environment

    python3.9 -m venv --prompt mindikatta __venv__
    pip install

## Database changes

Make changes in the `mindikatta/harvest/models.py` file then

    make models
    make tests

and then run:

    python manage.py migrate

## Deployment

### Update `docker buildx`

Beacuse we're building for Raspberry Pi (arm64) architecute we need to use `docker buildx`, which means we need to update local buildx to add arm64 architecture build target 

From [Building Multi-Arch Images for Arm and x86 with Docker Desktop](https://www.docker.com/blog/multi-arch-images/)

    docker buildx create --name mybuilder
    docker buildx use mybuilder
    docker buildx inspect --bootstrap

then we should be able to 

    make image
    make push

to build the image and then push it to Dockerhub

## Feature Requests

- "would be good to be able to go into each type of nut to see the individual entries"
- Graph current year vs historical average
- Linear regression

## Bugs

- Timezone differences between DB and Pandas