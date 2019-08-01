# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Blueprint used for loading templates."""

from __future__ import absolute_import, print_function

from flask import Blueprint

blueprint = Blueprint(
    'invenio_app_ils',
    __name__,
    template_folder='templates',
    static_folder='static',
)
