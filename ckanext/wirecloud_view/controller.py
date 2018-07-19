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

from __future__ import unicode_literals

import json
import os
from urlparse import urljoin
from urllib import quote_plus

from ckan.common import request, response
from ckan.lib import base
from ckan.plugins import toolkit, get_plugin
from requests_oauthlib import OAuth2Session
import six


class WireCloudViewController(base.BaseController):

    def __init__(self):
        self.client_id = six.text_type(os.environ.get('CKAN_OAUTH2_CLIENT_ID', toolkit.config.get('ckan.oauth2.client_id', ''))).strip()

    def get_workspaces(self):

        q = request.params.get('incomplete', '')
        limit = request.params.get('limit', '10')

        plugin = get_plugin('wirecloud_view')

        # Create a OAuth2 Session
        token = toolkit.c.usertoken
        oauth = OAuth2Session(self.client_id, token=token)
        # Request workspaces
        wirecloud_response = oauth.get(urljoin(plugin.wirecloud_url, "api/search") + "?namespace=workspace&q=" + quote_plus(q) + "&maxresults=" + quote_plus(limit))
        dashboards = wirecloud_response.json()['results']

        response.headers[b'Content-Type'] = b"application/json"
        return json.dumps({
            "ResultSet": {
                "Result": [{"Name": "%s/%s" % (dashboard['owner'], dashboard['name'])} for dashboard in dashboards]
            }
        }).encode("utf-8")
