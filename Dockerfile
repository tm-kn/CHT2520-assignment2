FROM python:3.6.6-stretch

RUN useradd timetracker

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=timetracker.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -"

EXPOSE 8000

RUN apt-get update -y && \
    apt-get install -y apt-transport-https rsync && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - &&\
    apt-get install -y nodejs &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn== 19.9.0"

COPY --chown=timetracker package.json package-lock.json ./
RUN npm install

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY --chown=timetracker webpack.config.js .
COPY --chown=timetracker timetracker/static ./timetracker/static
RUN npm run build

WORKDIR /app

COPY --chown=timetracker . .

RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

USER timetracker

CMD gunicorn timetracker.wsgi:application
