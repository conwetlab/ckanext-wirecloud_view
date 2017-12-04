# -*- coding: utf-8 -*-

# Copyright (c) 2017 Future Internet Consulting and Development Solutions S.L.

# This file is part of CKAN WireCloud View Extension.

# CKAN WireCloud View Extension is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN WireCloud View Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN WireCloud View Extension. If not, see <http://www.gnu.org/licenses/>.
# This file is part of CKAN Data Requests Extension.

import unittest

from ckan.plugins.toolkit import Invalid
from mock import MagicMock, patch
import six

import ckanext.wirecloudview.plugin as plugin


class WirecloudViewPluginTest(unittest.TestCase):

    def test_process_dashboardid_should_strip(self):

        self.assertEqual(plugin.process_dashboardid("  owner/name ", {}), "owner/name")

    def test_process_dashboardid_should_leave_untouched_valid_dashboard_ids(self):

        self.assertEqual(plugin.process_dashboardid("owner/name", {}), "owner/name")

    def test_process_dashboardid_should_raise_invalid_exception(self):

        with self.assertRaises(Invalid):
            plugin.process_dashboardid("a/b/c", {})

    def test_can_view_returns_false(self):
        instance = plugin.WirecloudView()
        self.assertFalse(instance.can_view({}))

    def test_get_helpers(self):
        instance = plugin.WirecloudView()
        helpers = instance.get_helpers()

        for key, helper in six.iteritems(helpers):
            self.assertTrue(callable(helper))

    def test_info_returns_dict(self):
        instance = plugin.WirecloudView()
        self.assertTrue(isinstance(instance.info(), dict))

    def test_form_template(self):
        instance = plugin.WirecloudView()
        self.assertEqual(instance.form_template(None, None), "wirecloud_form.html")

    def test_view_template(self):
        instance = plugin.WirecloudView()
        self.assertEqual(instance.view_template(None, None), "wirecloud_view.html")
