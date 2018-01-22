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

"""E-Ternity SIPStore utils module."""

from invenio_archivematica.models import Archive


def archive_directory_builder(sip):
    """Build a directory structure for the archived SIP.

    Creates a structure that is based on the Archive object linked to the SIP.
    It takes its accession_id. In case no Archive object exists, it returns
    the ID of the SIP.
    :param sip: SIP which is to be archived
    :type SIP: invenio_sipstore.models.SIP
    :returns: list of str
    """
    ark = Archive.get_from_sip(sip.id)
    if not ark and not ark.accession_id:
        return [str(sip.id)]
    return [ark.accession_id]
