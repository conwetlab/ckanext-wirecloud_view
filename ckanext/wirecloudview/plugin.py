# -*- coding: utf-8 -*-

# Copyright (c) 2015 CoNWeT Lab., Universidad Politécnica de Madrid

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
import db
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

url_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

GET = dict(method=['GET'])
PUT = dict(method=['PUT'])
POST = dict(method=['POST'])
DELETE = dict(method=['DELETE'])

if wirecloud_url[-1:] != "/":
    wirecloud_url += "/"


class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    def process_url(self, url, context):

        if not url:
            # The database may not be initialized
            db.init_db(model)

            # Handle the dashboard creation made with the Wizard
            res_id = request.url.split('/')[6]
            view_id = request.POST.get('view_id', '')

            dashboard = db.Dashboard.by_resource_and_view(res_id, view_id)

            if dashboard:
                url = wirecloud_url + dashboard.dashboard_path

                # Once that the view is created this information is no longer needed
                # so we can delete the database entry
                model.Session.delete(dashboard)

        if not url_re.match(url):
            raise Invalid('This field must contain a valid url.')

        # if not wirecloud_url in url:
        #    raise Invalid('The url must come from Wirecloud.')

        # Use the embedded mode
        if "?mode=embedded" not in url:
            url += "?mode=embedded"

        return url

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('fanstatic', 'wirecloud_typeahead')
        p.toolkit.add_resource('fanstatic', 'wirecloud_option')
        p.toolkit.add_resource('fanstatic', 'wirecloud_view')

    def info(self):
        return {'name': 'wirecloud_view',
                'title': 'Wirecloud',
                'icon': 'bar-chart',
                'schema': {'wirecloud_url': [unicode, self.process_url],
                           'view_id': [unicode]},
                'iframed': False,
                'always_available': True,
                'default_title': 'Wirecloud'
                }

    def can_view(self, data_dict):
        # If someone adds this view to default_views to avoid an empty iframe
        return False

    def view_template(self, context, data_dict):
        log.debug("view_template CALLED")
        return 'wirecloud_view.html'

    def form_template(self, context, data_dict):
        self.view_id = int(round(random.random() * 10000))
        log.debug("View id: " + str(self.view_id))
        return 'wirecloud_form.html'

    def get_view_id(self):
        return str(self.view_id)

    def get_helpers(self):

        def _get_workspaces():

            token = p.toolkit.c.usertoken   # get the token from oauth2 plugin
            oauth = OAuth2Session(client_id, token=token)
            response = oauth.get(wirecloud_url + "api/workspaces" + '?access_token=%s' % token['access_token']) #make the request
            return response.text

        return {
            'get_workspaces': _get_workspaces,
            'get_base_url': lambda: wirecloud_url,
            'get_editor_url': lambda: urljoin(wirecloud_url, editor_dashboard),
            'get_view_id': lambda: str(self.view_id)
        }

    def before_map(self, m):
        # FIXME: Include all the content in the body of the request
        m.connect('/wirecloud_view/resource/{resource_id}/view/{view_id}/workspace/{dashboard_path:.* ?}',
                  controller='ckanext.wirecloudview.plugin:WirecloudViewController',
                  action='notify_dashboard_path', conditions=POST)

        return m


class WirecloudViewController(base.BaseController):

    def notify_dashboard_path(self, resource_id, view_id, dashboard_path):

        # The database may not be initialized
        db.init_db(model)

        dashboard = db.Dashboard()
        dashboard.resource_id = resource_id
        dashboard.view_id = view_id
        dashboard.dashboard_path = dashboard_path

        model.Session.add(dashboard)
        model.Session.commit()
