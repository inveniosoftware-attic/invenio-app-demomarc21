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

"""Default configuraiton for Integrated Library System flavour of Invenio.

The following is an overview of the default ILS configuration for Invenio.
You may customize the default configuration. Please refer to
http://invenio.readthedocs.io/en/latest/usersguide/tutorial/customize.html
for a tutorial on how to customize Invenio.
"""

from __future__ import absolute_import, print_function

from datetime import timedelta

from invenio_marc21.config import MARC21_REST_ENDPOINTS, MARC21_UI_ENDPOINTS, \
    MARC21_UI_EXPORT_FORMATS
from invenio_records_rest.facets import range_filter, terms_filter


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
#: Global base template.
BASE_TEMPLATE = 'invenio_theme/page.html'
#: Cover page base template (used for e.g. login/sign-up).
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
#: Footer base template.
FOOTER_TEMPLATE = 'invenio_theme/footer.html'
#: Header base template.
HEADER_TEMPLATE = 'invenio_theme/header.html'
#: Settings base template.
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('Invenio')
#: Use default frontpage.
THEME_FRONTPAGE = True
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('Integrated Library System')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'e_ternity/frontpage.html'

# Assets
# ======
#: Static files colleciton method (defaults to copying files).
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
    )
)

#: Default sort for records REST API.
RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(query='bestmatch', noquery='mostrecent'),
)

#: Defined facets for records REST API.
RECORDS_REST_FACETS = dict(
    marc21=dict(
        aggs=dict(
            identifier=dict(
                terms=dict(
                    field='other_standard_identifier.source_of_number_or_code'
                ),
            ),
            language=dict(
                terms=dict(
                    field=('language_code.language_code_of_text_sound_track_or'
                           '_separate_title')
                )
            ),
            affiliation=dict(
                terms=dict(
                    field='main_entry_personal_name.affiliation'
                )
            ),
            years=dict(
                date_histogram=dict(
                    field='_created',
                    interval='year',
                    format='yyyy'
                )
            )
        ),
        post_filters=dict(
            identifier=terms_filter(
                'other_standard_identifier.source_of_number_or_code'
            ),
            language=terms_filter(
                ('language_code.language_code_of_text_sound_track_or'
                 '_separate_title')
            ),
            affiliation=terms_filter(
                'main_entry_personal_name.affiliation'
            ),
            years=range_filter(
                '_created',
                format='yyyy',
                end_date_math='/y'
            ),
        )
    )
)

# TODO: Remove once schema validation issue is fixed.
INDEXER_DEFAULT_INDEX = 'marc21-bibliographic-bd-v1.0.0'
INDEXER_DEFAULT_DOCTYPE = 'bd-v1.0.0'

# TODO: Remove me once the problem with email is solved in flask-security:
# https://github.com/mattupstate/flask-security/issues/685
SECURITY_EMAIL_SENDER = 'no-reply@localhost'

# OAI-PMH Server
# ==============
#: Elasticsearch index to serve OAI-PMH server from.
OAISERVER_RECORD_INDEX = 'marc21'

# Celery configuration
# ====================
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
# Celery 4 requires different config names
CELERY_BEAT_SCHEDULE = CELERYBEAT_SCHEDULE
"""Task schedule for Celery.

By default we run bulk indexing every 5 minutes and session table clean up
every hour.
"""

SEARCH_UI_JSTEMPLATE_FACETS = 'templates/invenio_search_ui/facets.html'
"""Configure the facets template."""
