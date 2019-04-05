time tracker
============

This is a web application of a web tracker written in Python using the Django
web framework.

The app is live at http://quiet-crag-93436.herokuapp.com/.
Student ID - 1562595.


Set up local environment
------------------------

Requirements to run the project VM are:

- Vagrant
- VirtualBox

.. code:: sh

   vagrant up
   vagrant ssh

The VM comes with aliases:

-  ``dj`` - shortcut to ``django-admin``
-  ``djrun`` - shortcut to ``django-admin runserver 0:8000``
-  ``djcelery`` - to start the Celery process.

Create database and superuser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   vagrant ssh
   dj migrate
   dj createsuperuser

Start the development server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   vagrant ssh
   djrun

The application should be available at http://localhost:8000/.


Compile static files
~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   vagrant ssh
   npm install
   npm run build

To run a front-end watcher use ``npm start``.


Run tests
~~~~~~~~

.. code:: sh

   vagrant ssh
   dj test

Deployment
~~~~~~~~~~

This app supports deployment on Heroku with the container stack. To accomplish
that please use the following command to create a new deployment.

.. code:: sh

   heroku apps:create --region eu --stack container
   heroku addons:create heroku-postgresql
   heroku addons:create papertrail
   heroku addons:create heroku-scheduler
   heroku addons:create sentry
   heroku addons:add heroku-redis --as CELERY_BROKER
   heroku config:set SECRET_KEY=[your-secret-key] ALLOWED_HOSTS=*.herokuapp.com
   heroku config:set AWS_STORAGE_BUCKET_NAME=[your bucket name] \
                     AWS_ACCESS_KEY_ID=[your key id] \
                     AWS_SECRET_ACCESS_KEY=[your access key] \
                     AWS_S3_REGION_NAME=eu-west-2
   heroku config:set EMAIL_HOST=smtp.mailgun.org \
                     EMAIL_PORT=587 \
                     EMAIL_HOST_PASSWORD=[smtp password] \
                     EMAIL_HOST_USER=[smtp user] \
                     EMAIL_USE_TLS=True \
                     EMAIL_SUBJECT_PREFIX=[timetracker] \
                     SERVER_EMAIL=no-reply@yourdomain.com
   git push heroku
