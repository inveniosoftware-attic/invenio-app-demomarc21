# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""E2E integration tests."""

from flask import url_for


def test_login_unknown_user_get_error(live_server, browser, app):
    """Test that a login for an unknown user fails."""

    username = 'test@test.com'
    ds = app.extensions['invenio-accounts'].datastore

    with app.app_context():
        user = ds.find_user(email=username)
        if user:
            ds.delete_user()
            ds.commit()

        _login(browser, username, 'password')

        assert browser.find_element_by_xpath(
            "//div[contains(@class, 'alert')]/p").text == 'Specified user ' \
                                                          'does not exist'


def _login(browser, username, password):
    browser.get(url_for('invenio_theme_frontpage.index', _external=True))
    browser.find_element_by_xpath("//a[contains(@href, '/login/')]").click()

    browser.find_element_by_id("email").clear()
    browser.find_element_by_id("email").send_keys(username)
    browser.find_element_by_id("password").clear()
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_xpath("//button[@type='submit']").click()
