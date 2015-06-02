import logging
import ckan.plugins as p
from ckan.plugins.toolkit import Invalid
import re
from requests_oauthlib import OAuth2Session
import pylons.config as config
import json

log = logging.getLogger(__name__)
wcURL = config.get('ckan.wirecloud_view.url', False)
client_id = config.get('ckan.oauth2.client_id', False)

if wcURL[-1:] != "/":
    wcURL += "/"

def process_url(url):
    if not re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        raise Invalid('This field must contain a valid url.')
    return url

def get_base_url():
    return wcURL

def get_workspaces():
    log.debug("GET WORKSPACES()")   
    
    token = p.toolkit.c.usertoken
    oauth = OAuth2Session(client_id, token=token)    
    response = oauth.get(wcURL + "api/workspaces" + '?access_token=%s' % token['access_token'])        
    workspaces = response.text

    return workspaces

class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)
    p.implements(p.ITemplateHelpers)    

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('fanstatic', 'wirecloud_typeahead')


    def info(self):
        return {'name': 'wirecloud_view',
                'title': 'Wirecloud',
                'icon': 'bar-chart',
                'schema': {'wirecloud_url': [unicode, process_url]},
                'iframed': False,
                'always_available': True,
                'default_title': 'Wirecloud'
                }

    def can_view(self, data_dict):
        return False #If someone adds this view to default_views to avoid an empty iframe

    def view_template(self, context, data_dict):
        return 'wirecloud_view.html'

    def form_template(self, context, data_dict):        
        return 'wirecloud_form.html'

    def get_helpers(self):
        return {'get_workspaces': get_workspaces,
                'get_base_url': get_base_url}