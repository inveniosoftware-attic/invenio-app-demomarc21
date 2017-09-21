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

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.4.1',
    'isort>=4.2.15',
    'pydocstyle>=2.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=2.5.1',
    'pytest-pep8>=1.0.6',
    'pytest>=3.1.3',
    'pytest-flask>=0.10.0',
    'selenium>=3.4.3',
]

invenio_db_version = '>=1.0.0b8,<1.1.0'

extras_require = {
    # Databases
    'mysql': [
        'invenio-db[mysql]' + invenio_db_version,
    ],
    'postgresql': [
        'invenio-db[postgresql]' + invenio_db_version,
    ],
    # Elasticsearch versionS
    'elasticsearch2': [
        'elasticsearch>=2.0.0,<3.0.0',
        'elasticsearch-dsl>=2.0.0,<3.0.0',
    ],
    'elasticsearch5': [
        'elasticsearch>=5.0.0,<6.0.0',
        'elasticsearch-dsl>=5.0.0,<6.0.0',
    ],
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('mysql', 'postgresql', 'elasticsearch2', 'elasticsearch5'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    # Base bundle
    'invenio-admin>=1.0.0b4',
    'invenio-assets>=1.0.0b6',
    'invenio-base>=1.0.0a16',
    'invenio-celery>=1.0.0b3',
    'invenio-cache>=1.0.0b1',
    'invenio-config>=1.0.0b3',
    'invenio-formatter>=1.0.0b3',
    'invenio-i18n>=1.0.0b4',
    'invenio-logging>=1.0.0b3',
    'invenio-mail>=1.0.0b1',
    'invenio-rest[cors]>=1.0.0b1',
    'invenio-theme>=1.0.0b4',
    # Auth bundle
    'invenio-access>=1.0.0b1',
    'invenio-accounts>=1.0.0b10',
    'invenio-oauth2server>=1.0.0b1',
    'invenio-oauthclient>=1.0.0b2',
    'invenio-userprofiles>=1.0.0b1',
    # Metadata bundle
    'invenio-indexer>=1.0.0a10',
    'invenio-jsonschemas>=1.0.0a5',
    'invenio-oaiserver>=1.0.0a13',
    'invenio-pidstore>=1.0.0b2',
    'invenio-records-rest>=1.0.0b1',
    'invenio-records-ui>=1.0.0b1',
    'invenio-records>=1.0.0b2',
    'invenio-search-ui>=1.0.0a7',
    'invenio-search>=1.0.0a10',
    # # Files bundle
    'invenio-records-files>=1.0.0a9',
    # Archive bundle
    # FIXME put a real version when a release has been done
    # and remove the "dependency_links" line below
    # along with the "--process-dependency-links" option in the Dockerfile
    # and in the .travis.yml file
    'invenio-archivematica>=0.1.0.dev20170825',
    # MARC21-based ILS
    'invenio-app>=1.0.0b1',
    'invenio-marc21>=1.0.0a5',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('e_ternity', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='e-ternity',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio ils library system',
    license='GPLv2',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/remileduc/e-ternity',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'flask.commands': [
            'demo = e_ternity.cli:demo',
            'marc21 = e_ternity.cli:marc21_cli',
        ],
        'invenio_base.blueprints': [
            'e_ternity = e_ternity.views:blueprint',
        ],
        'invenio_config.module': [
            'e_ternity = e_ternity.config',
        ],
        'invenio_i18n.translations': [
            'messages = e_ternity',
        ],
    },
    dependency_links=['https://github.com/inveniosoftware/invenio-archivematica/tarball/master#egg=invenio-archivematica-0.1.0.dev20170825'],
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)
