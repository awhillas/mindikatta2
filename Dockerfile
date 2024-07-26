FROM python:3.9-slim-bookworm AS app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    DJANGO_SETTINGS_MODULE="config.production"

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "-w", "4", "--worker-tmp-dir", "/dev/shm", "mindikatta.wsgi"]