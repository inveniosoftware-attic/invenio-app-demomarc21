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

"""Integrated Library System flavour of Invenio."""

from __future__ import absolute_import, print_function

import uuid

import click
import pkg_resources
from dojson.contrib.marc21 import marc21, marc21_authority
from dojson.contrib.marc21.utils import create_record, load, split_stream
from flask.cli import with_appcontext
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records.api import Record


def import_records(dojson_model, schema, xmlfile):
    """Helper to import a MARCXML file for given schema."""
    ids = []
    from invenio_pidstore import current_pidstore
    with db.session.begin_nested():
        with open(xmlfile, 'rb') as fp:
            for item in load(fp):
                # Transform MARCXML to JSON
                data = dojson_model.do(item)
                # TODO: Add schema once schema validation has been fixed.
                # Schema
                # data['$schema'] = schema
                # Create a UUID for the record
                id_ = uuid.uuid4()
                # FIXME: Strip off control number otherwise minter will fail.
                if 'control_number' in data:
                    del data['control_number']
                # Mint a recid and OAI id.
                pid = current_pidstore.minters['recid'](id_, data)
                current_pidstore.minters['oaiid'](id_, data)
                # Store record.
                record = Record.create(data, id_=id_)
                click.echo('Created record {}'.format(pid.pid_value))
                ids.append(id_)
    return ids


@click.group('marc21')
def marc21_cli():
    """MARC21 related commands."""


@marc21_cli.command('import')
@with_appcontext
@click.argument('input', type=click.Path(
    exists=True, file_okay=True, dir_okay=True, readable=True))
@click.option(
    '--bibliographic', 'dojson_model', flag_value=marc21, default=True)
@click.option(
    '--authority', 'dojson_model', flag_value=marc21_authority)
def marc21_import(dojson_model, input):
    """Import MARCXML records."""
    from flask import current_app
    if dojson_model == marc21:
        schema = current_app.extensions['invenio-jsonschemas'].path_to_url(
            'marc21/bibliographic/bd-v1.0.0.json')
    elif dojson_model == marc21_authority:
        schema = current_app.extensions['invenio-jsonschemas'].path_to_url(
            'marc21/authority/ad-v1.0.0.json')

    # Create records
    click.secho('Importing records', fg='green')
    record_ids = import_records(dojson_model, schema, input)
    db.session.commit()

    # Index records
    click.secho('Indexing records', fg='green')
    indexer = RecordIndexer()
    indexer.bulk_index(record_ids)
    indexer.process_bulk_queue()


@click.group()
def demo():
    """Demo-site commands."""


@demo.command('init')
@with_appcontext
def demo_init():
    """Initialize demo site."""
    from flask import current_app
    records = []
    # Import bibliographic records
    click.secho('Importing bibliographic records', fg='green')
    records += import_records(
        marc21,
        current_app.extensions['invenio-jsonschemas'].path_to_url(
            'marc21/bibliographic/bd-v1.0.2.json'),
        pkg_resources.resource_filename(
            'invenio_records', 'data/marc21/bibliographic.xml'),
    )
    # FIXME add support for authority records.
    # Import authority records
    # click.secho('Importing authority records', fg='green')
    # records += import_records(
    #     marc21_authority,
    #     current_app.extensions['invenio-jsonschemas'].path_to_url(
    #         'marc21/authority/ad-v1.0.2.json'),
    #     pkg_resources.resource_filename(
    #         'invenio_records', 'data/marc21/authority.xml'),
    # )
    db.session.commit()
    # Index all records
    click.secho('Indexing records', fg='green')
    indexer = RecordIndexer()
    indexer.bulk_index(records)
    indexer.process_bulk_queue()
