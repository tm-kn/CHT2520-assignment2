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
