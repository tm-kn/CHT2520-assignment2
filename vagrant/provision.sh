#!/bin/sh
set -xe

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


set +e
su - vagrant -c "createdb $PROJECT_NAME"
set -e


# Virtualenv setup for project
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"
su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"
su - vagrant -c "$PIP install --upgrade pip"
su - vagrant -c "$PIP install --upgrade setuptools"
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements-dev.txt"

# .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev
export DATABASE_URL=postgres:///$PROJECT_NAME

alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"
alias djcelery="celery -A timetracker worker -l info"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF

# Install node.js and npm
curl -sSL https://deb.nodesource.com/setup_11.x | bash -
apt-get install -y nodejs

# Compile static
su - vagrant -c "cd $PROJECT_DIR && npm i"
su - vagrant -c "cd $PROJECT_DIR && make static"
