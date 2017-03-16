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

import copy
from datetime import timedelta

from invenio_marc21.config import MARC21_REST_ENDPOINTS, MARC21_UI_ENDPOINTS, \
    MARC21_UI_EXPORT_FORMATS
from invenio_records_rest.facets import terms_filter


def _(x):
    """Identity function used to trigger string extraction."""
    return x

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
#: Other supported languages (do not include default language in list).
I18N_LANGUAGES = [
    ('fr', _('French'))
]

# Base templates
# ==============
# ADMIN_BASE_TEMPLATE = 'invenio_theme/page_admin.html'
BASE_TEMPLATE = 'invenio_theme/page.html'
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
FOOTER_TEMPLATE = 'invenio_theme/footer.html'
HEADER_TEMPLATE = 'invenio_theme/header.html'
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# Theme configuration
# ===================
THEME_SITENAME = _('Invenio')
THEME_FRONTPAGE = True
THEME_FRONTPAGE_TITLE = _('Integrated Library System')
THEME_FRONTPAGE_TEMPLATE = 'invenio_app_ils/frontpage.html'

# Assets
# ======
# Static files colleciton method (defaults to copying files).
COLLECT_STORAGE = 'flask_collect.storage.file'

# Records configuration
# =====================
#: Records UI configuration
RECORDS_UI_ENDPOINTS = {}
RECORDS_UI_ENDPOINTS.update(MARC21_UI_ENDPOINTS)

#: Records UI export format and serializer configuration.
RECORDS_UI_EXPORT_FORMATS = {}
RECORDS_UI_EXPORT_FORMATS.update(MARC21_UI_EXPORT_FORMATS)

#: Records REST API configuration
RECORDS_REST_ENDPOINTS = {}
RECORDS_REST_ENDPOINTS.update(MARC21_REST_ENDPOINTS)

#: Records REST sort options
RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            fields=['-_score'],
            title='Best match',
            default_order='asc',
            order=1,
        ),
        mostrecent=dict(
            fields=['-_created'],
            title='Most recent',
            default_order='asc',
            order=2,
        ),
        title=dict(
            fields=['title_statement.title', ],
            title='Title',
            order=3,
        ),
    )
)

#: Default sort for records REST API.
RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(query='bestmatch', noquery='mostrecent'),
)

#: Defined facets for records REST API.
RECORDS_REST_FACETS = dict(
    records=dict(
        aggs=dict(
            author=dict(
                terms=dict(field="main_entry_personal_name.personal_name"),
            ),
        ),
        post_filters=dict(
            author=terms_filter('main_entry_personal_name.personal_name'),
        )
    )
)

# TODO: Remove once schema validation issue is fixed.
INDEXER_DEFAULT_INDEX = 'marc21-bibliographic-bd-v1.0.0'
INDEXER_DEFAULT_DOCTYPE = 'bd-v1.0.0'

# OAI-PMH Server
# ==============
OAISERVER_RECORD_INDEX = 'marc21'

# Celery configuration
# ====================
#: Beat schedule
CELERYBEAT_SCHEDULE = {
    'indexer': {
        'task': 'invenio_indexer.tasks.process_bulk_queue',
        'schedule': timedelta(minutes=5),
    },
    'accounts': {
        'task': 'invenio_accounts.tasks.clean_session_table',
        'schedule': timedelta(minutes=60),
    },
}
