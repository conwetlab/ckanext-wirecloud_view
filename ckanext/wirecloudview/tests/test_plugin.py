"""Tests for plugin.py."""
import ckanext.wirecloudview.plugin as plugin

from mock import MagicMock, patch


class DataRequestPluginTest(unittest.TestCase):

    def test_process_dashboardid_should_strip(self):

        self.assertEqual(plugin.process_dashboardid(self, "  owner/name ", context), "onwer/name")

    def test_process_dashboardid_should_leave_untouched_valid_dashboard_ids(self):

        self.assertEqual(plugin.process_dashboardid(self, "owner/name", context), "onwer/name")
