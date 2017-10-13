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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os

import pytest
from invenio_app.factory import create_app
from invenio_db import db as db_
from sqlalchemy_utils.functions import create_database, database_exists


@pytest.fixture(scope='module', autouse=True)
def base_app(tmpdir_factory):
    """Flask application fixture."""
    tmpdir = tmpdir_factory.mktemp('data')
    sqlite = 'sqlite:///{filepath}'.format(
        filepath=tmpdir.join('unit-test.db')
    )

    app_ = create_app(
        DEBUG_TB_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            sqlite),
        SECRET_KEY="CHANGE_ME",
        SECURITY_PASSWORD_SALT="CHANGE_ME",
        TESTING=True,
        DEBUG=True,
    )

    with app_.app_context():
        yield app_


@pytest.fixture(scope='module')
def db():
    """Setup database."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()

    yield db_

    db_.session.remove()
    db_.drop_all()


@pytest.fixture()
def app(base_app, db):
    """Flask application fixture."""
    yield base_app
