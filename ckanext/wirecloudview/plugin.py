import logging
import ckan.plugins as p
from ckan.plugins.toolkit import Invalid
import re
from requests_oauthlib import OAuth2Session
import pylons.config as config
import json
from ckan.controllers.package import PackageController
from ckan.common import request

import random

log = logging.getLogger(__name__)
wcURL = config.get('ckan.wirecloud_view.url', False)
editor_url = config.get('ckan.wirecloud_view.editor_url', False)
client_id = config.get('ckan.oauth2.client_id', False)

urls_from_editor = {}

url_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

GET = dict(method=['GET'])
PUT = dict(method=['PUT'])
POST = dict(method=['POST'])
DELETE = dict(method=['DELETE'])

if wcURL[-1:] != "/":
    wcURL += "/"

def get_base_url():
    return wcURL

def get_editor_url():
    return editor_url

def get_workspaces():

    token = p.toolkit.c.usertoken #get the token from oauth2 plugin
    oauth = OAuth2Session(client_id, token=token)
    response = oauth.get(wcURL + "api/workspaces" + '?access_token=%s' % token['access_token']) #make the request
    workspaces = response.text

    return workspaces

class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IRoutes, inherit=True)

    def process_url(self, url, context):

        res_id = context['resource'].id
        view_id = request.POST.get('view_id','')

        temp_id = res_id + '/' + view_id

        if temp_id in urls_from_editor:
            log.debug('URL retrieved from editor')
            url = wcURL + urls_from_editor[temp_id]
            del urls_from_editor[temp_id]

        if not url_re.match(url):
            raise Invalid('This field must contain a valid url.')

        #if not wcURL in url:
        #    raise Invalid('The url must come from Wirecloud.')

        if not "?mode=embedded" in url:
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
        return False #If someone adds this view to default_views to avoid an empty iframe

    def view_template(self, context, data_dict):
        log.debug("view_template CALLED")
        return 'wirecloud_view.html'

    def form_template(self, context, data_dict):
        self.view_id = int(round(random.random() * 10000))

        log.debug("form_template CALLED")
        log.debug("View id: " + `self.view_id`)

        return 'wirecloud_form.html'

    def get_view_id(self):
        return str(self.view_id)

    def get_helpers(self):
        return {'get_workspaces': get_workspaces,
                'get_base_url': get_base_url,
                'get_editor_url': get_editor_url,
                'get_view_id': self.get_view_id}

    def before_map(self, m):
        m.connect('/wirecloud_view/resource/{resource_id}/view/{view_id}/workspace/{wc_url:.* ?}',
                  controller='ckanext.wirecloudview.plugin:WirecloudViewController',
                  action='update_url', conditions=POST)
        return m

#TODO: How to read wc_url as a POST parameter instead of directly from URL path????
class WirecloudViewController(PackageController):

    def update_url(self, resource_id, view_id, wc_url): #view_id,

        urls_from_editor[resource_id+'/'+view_id] = wc_url
        log.debug("Update url called")
        log.debug(urls_from_editor)
        return wc_url