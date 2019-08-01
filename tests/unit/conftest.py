# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os

import pytest
from invenio_app.factory import create_ui


@pytest.fixture(scope='module')
def create_app():
    """Flask application fixture."""
    return create_ui
