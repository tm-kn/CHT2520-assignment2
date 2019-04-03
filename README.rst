time tracker
============

This is a web application of a web tracker written in Python using the Django
web framework.

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
   make static


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
   heroku config:set SECRET_KEY=[your-secret-key] ALLOWED_HOSTS=*.herokuapp.com
   git push heroku
