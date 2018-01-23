#!/usr/bin/env bash
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
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

invenio db destroy --yes-i-know
invenio db init create
invenio index queue init
invenio index init
invenio demo init

invenio files location --default records /records/
invenio files location archive /archive/

# Create a test user
invenio users create test@test.ch -a --password=123456
# Create an admin user
invenio users create admin@test.ch -a --password=123456
invenio roles create admin
invenio roles add admin@test.ch admin
invenio access allow superuser-access role admin
# Allow access to archive
invenio access allow archive-read user test@test.com
invenio access allow archive-write user test@test.com
