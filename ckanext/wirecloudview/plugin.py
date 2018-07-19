# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016 CoNWeT Lab., Universidad Politécnica de Madrid
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


import logging
import os
import pylons.config as config
import re
from urlparse import urljoin

import ckan.plugins as p
from ckan.plugins.toolkit import Invalid
from requests_oauthlib import OAuth2Session


log = logging.getLogger(__name__)
client_id = config.get('ckan.oauth2.client_id', False)

DASHBOARD_RE = re.compile('^[^/]+/[^/]+$')

GET = dict(method=['GET'])
PUT = dict(method=['PUT'])
POST = dict(method=['POST'])
DELETE = dict(method=['DELETE'])


def process_dashboardid(dashboardid, context):

    dashboardid = dashboardid.strip()

    if not DASHBOARD_RE.match(dashboardid):
        raise Invalid('This field must contain a valid dashboard id.')

    return dashboardid


class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    def configure(self, config):
        self.wirecloud_url = os.environ.get('CKAN_WIRECLOUD_VIEW_URL', config.get('ckan.wirecloud_view.url', 'https://mashup.lab.fiware.org'))
        self.editor_dashboard = os.environ.get('CKAN_WIRECLOUD_VIEW_EDITOR_DASHBOARD', config.get('ckan.wirecloud_view.editor_dashboard', 'wirecloud/ckan-editor'))

        if self.wirecloud_url[-1:] != "/":
            self.wirecloud_url += "/"

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource(b'fanstatic', b'wirecloud_view')

    def info(self):
        return {
            'name': 'wirecloud_view',
            'title': 'WireCloud',
            'icon': 'bar-chart-o' if p.toolkit.check_ckan_version(min_version='2.7') else 'bar-chart',
            'schema': {
                'dashboard': [unicode, process_dashboardid],
            },
            'iframed': False,
            'always_available': True,
            'default_title': 'WireCloud'
        }

    def can_view(self, data_dict):
        # If someone adds this view to default_views to avoid an empty iframe
        return False

    def view_template(self, context, data_dict):
        return 'wirecloud_view.html'

    def form_template(self, context, data_dict):
        return 'wirecloud_form.html'

    def get_helpers(self):

        return {
            'get_editor_url': lambda: urljoin(self.wirecloud_url, self.editor_dashboard),
            'get_dashboard_url': lambda dashboard, resourceid, ckanserver: urljoin(self.wirecloud_url, dashboard) + '?mode=embedded&resourceid=' + resourceid + '&ckanserver=' + ckanserver
        }

    def before_map(self, m):

        m.connect('/api/3/wirecloud_view/dashboard_autocomplete',
                  controller='ckanext.wirecloudview.controller:WireCloudViewController',
                  action='get_workspaces', conditions=GET)

        return m
