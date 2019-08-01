#!/usr/bin/env bash
#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

CWD=`pwd`
invenio npm
cd ${VIRTUAL_ENV}/var/instance/static
npm install
cd ${CWD}
invenio collect -v
invenio assets build
