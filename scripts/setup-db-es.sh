#!/usr/bin/env bash
#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

invenio db destroy --yes-i-know
invenio db init create
invenio index queue init
invenio index init
invenio demo init

