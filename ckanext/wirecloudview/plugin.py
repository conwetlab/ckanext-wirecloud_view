import logging
import ckan.plugins as p
from ckan.plugins.toolkit import Invalid
import re

log = logging.getLogger(__name__)

def is_url(url):
    if not re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        raise Invalid('This field must contain a valid url.')
    return url

class WirecloudView(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')


    def info(self):
        return {'name': 'wirecloud_view',
                'title': 'Wirecloud',
                'icon': 'bar-chart',
                'schema': {'wirecloud_url': [unicode, is_url]},
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