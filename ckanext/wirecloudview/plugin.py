# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016 CoNWeT Lab., Universidad Politécnica de Madrid

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


import ckan.lib.base as base
import ckan.model as model
import ckan.plugins as p
import logging
import pylons.config as config
import re
import random
from urlparse import urljoin


from ckan.plugins.toolkit import Invalid
from requests_oauthlib import OAuth2Session
from ckan.common import request


log = logging.getLogger(__name__)
wirecloud_url = config.get('ckan.wirecloud_view.url', 'https://mashup.lab.fiware.org')
editor_dashboard = config.get('ckan.wirecloud_view.editor_dashboard', 'wirecloud/ckan-editor')
client_id = config.get('ckan.oauth2.client_id', False)

DASHBOARD_RE = re.compile('^[^/]+/[^/]+$')

GET = dict(method=['GET'])
PUT = dict(method=['PUT'])
POST = dict(method=['POST'])
DELETE = dict(method=['DELETE'])

if wirecloud_url[-1:] != "/":
    wirecloud_url += "/"


def process_dashboardid(dashboardid, context):

    dashboardid = dashboardid.strip()

    if not DASHBOARD_RE.match(dashboardid):
        raise Invalid('This field must contain a valid dashboard id.')

    return dashboardid


class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('fanstatic', 'wirecloud_typeahead')
        p.toolkit.add_resource('fanstatic', 'wirecloud_option')
        p.toolkit.add_resource('fanstatic', 'wirecloud_view')

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

        def _get_workspaces():

            # Create a OAuth2 Session
            token = p.toolkit.c.usertoken
            oauth = OAuth2Session(client_id, token=token)
            # Request workspaces
            response = oauth.get(wirecloud_url + "api/workspaces" + '?access_token=%s' % token['access_token'])
            return response.text

        return {
            'get_workspaces': _get_workspaces,
            'get_editor_url': lambda: urljoin(wirecloud_url, editor_dashboard),
            'get_dashboard_url': lambda dashboard, resourceid, ckanserver: urljoin(wirecloud_url, dashboard) + '?mode=embedded&resourceid=' + resourceid + '&ckanserver=' + ckanserver
        }

    def before_map(self, m):
        # FIXME: Include all the content in the body of the request
        m.connect('/wirecloud_view/resource/{resource_id}/view/{view_id}/workspace/{dashboard_path:.* ?}',
                  controller='ckanext.wirecloudview.plugin:WirecloudViewController',
                  action='notify_dashboard_path', conditions=POST)

        return m
