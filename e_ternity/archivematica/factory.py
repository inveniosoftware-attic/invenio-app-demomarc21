# -*- coding: utf-8 -*-
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

"""E-Ternity sipstore utils modules."""

from flask import current_app
from invenio_records.api import Record
from invenio_sipstore.models import RecordSIP


def create_accession_id(ark):
    """Create an accession ID to store the sip in Archivematica.

    :param ark: the archive
    :type ark: :py:class:`invenio_archivematica.models.Archive`
    :returns: the created ID: `{SERVICE}-{NAME}`.
        Where `{SERVICE}` comes from `ARCHIVEMATICA_ORGANIZATION_NAME`,
        and `{NAME}` is the PID and the version of the associated record if
        there is one, or the ID of the SIP otherwise.
    :rtype: str
    """
    service = current_app.config['ARCHIVEMATICA_ORGANIZATION_NAME']
    recordsip = RecordSIP.query.filter_by(sip_id=ark.sip.id).one_or_none()
    if not recordsip:
        return service + '-' + str(ark.sip.id)
    rec = Record.get_record(recordsip.pid.get_assigned_object())
    return '{SERVICE}-{PIDTYPE}-{PID}-{REVISION}'.format(
        SERVICE=service,
        PIDTYPE=recordsip.pid.object_type,
        PID=recordsip.pid.pid_value,
        REVISION=rec.revision_id)
