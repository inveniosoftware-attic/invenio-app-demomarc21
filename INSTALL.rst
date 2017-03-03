Installation
============

Upgrade pip, setuptools and wheel to make sure you have latest versions:

.. code-block:: console

    $ mkvirtualenv ils
    $ pip install --upgrade pip setuptools wheel

Install Invenio ILS:

.. code-block:: console

   $ mkvirtualenv ils
   $ pip install --upgrade pip setuptools wheel
   $ pip install invenio-app-ils[postgresql,elasticsearch2]

Install web assets (JavaScript and CSS dependencies):

.. code-block:: console

   $ invenio npm
   $ cdvirtualenv var/instance/static/
   $ npm install

Build web assets and collect static files:

.. code-block:: console

   $ invenio collect -v
   $ invenio assets build

Create the database tables:

.. code-block:: console

   $ invenio db init
   $ invenio db create

Create the search indexes and indexing queue:

.. code-block:: console

    $ invenio index init
    $ invenio index queue init

Demo data
---------
You can load demo data by simply running:

.. code-block:: console

    $ invenio demo init
