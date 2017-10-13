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

"""Module tests."""

from __future__ import absolute_import, print_function


def test_version():
    """Test version import."""
    from invenio_app_ils import __version__
    assert __version__


def test_import_export(app):
    """Test importing all demo records and exporting to all formats."""
    import pkg_resources
    from dojson.contrib.marc21 import marc21
    from invenio_app_ils.cli import import_records
    from invenio_pidstore.models import PersistentIdentifier

    with app.app_context():
        # import all demo records
        import_records(
            marc21,
            app.extensions['invenio-jsonschemas'].path_to_url(
                'marc21/bibliographic/bd-v1.0.2.json'
            ),
            pkg_resources.resource_filename(
                'invenio_records',
                'data/marc21/bibliographic.xml'
            )
        )

        # export all records to marcxml, DublinCore, MODS, JSON
        export_formats = ['marcxml', 'mods', 'dc', 'json']
        recids = [x.pid_value
                  for x
                  in PersistentIdentifier.query.filter(
                    PersistentIdentifier.pid_type == 'recid'
                  ).all()
                  ]
        with app.test_client() as client:
            for recid in recids:
                for fmt in export_formats:
                    res = client.get(
                        "/record/{0}/export/{1}".format(recid, fmt)
                    )
                    assert res.status_code == 200
