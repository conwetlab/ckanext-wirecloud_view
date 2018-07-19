# -*- coding: utf-8 -*-

# Copyright (c) 2018 Future Internet Consulting and Development Solutions S.L.

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

import json
import unittest

from mock import DEFAULT, patch

from ckanext.wirecloudview.controller import WireCloudViewController


class WirecloudViewControllerTest(unittest.TestCase):

    @patch.multiple("ckanext.wirecloudview.controller", request=DEFAULT, get_plugin=DEFAULT, toolkit=DEFAULT, OAuth2Session=DEFAULT, response=DEFAULT)
    def test_get_workspaces(self, request, get_plugin, toolkit, OAuth2Session, response):
        self.controller = WireCloudViewController()
        self.controller.client_id = "aclientid"

        request.params = {
            'incomplete': 'key words',
            'limit': '20',
        }
        get_plugin().wirecloud_url = "https://dashboards.example.org"
        oauth = OAuth2Session()
        OAuth2Session.reset_mock()
        oauth.get().json.return_value = {
            "results": [
                {"owner": "user1", "name": "dashboard1"},
                {"owner": "user2", "name": "other-dashboard"},
            ]
        }
        oauth.get.reset_mock()
        response.headers = {}

        result = self.controller.get_workspaces()

        self.assertEqual(
            json.loads(result.decode('utf-8')),
            {
                "ResultSet": {
                    "Result": [
                        {"Name": "user1/dashboard1"},
                        {"Name": "user2/other-dashboard"},
                    ]
                }
            }
        )
        self.assertEqual(response.headers[b'Content-Type'], b"application/json")
        OAuth2Session.assert_called_once_with(self.controller.client_id, token=toolkit.c.usertoken)
        oauth.get.assert_called_once_with("https://dashboards.example.org/api/search?namespace=workspace&q=key+words&maxresults=20")
