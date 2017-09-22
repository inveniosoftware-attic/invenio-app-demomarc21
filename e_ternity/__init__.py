# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Integrated Library System flavour of Invenio.

Running
-------
Starting a development server is as simple as:

.. code-block:: console

    $ export FLASK_DEBUG=1
    $ invenio run


.. note::

   You must enable the debug mode as done above to prevent that all
   connections are forced to HTTPS since the development server does not work
   with HTTPS.

Celery workers can be started using the command:

.. code-block:: console

    $ celery worker -A invenio_app.celery -l INFO

An interactive Python shell is started with the command:

.. code-block:: console

    $ invenio shell

Demo data
---------
You can load demo data by simply running:

.. code-block:: console

    $ invenio demo init

"""

from __future__ import absolute_import, print_function

from .version import __version__

__all__ = ('__version__', )
