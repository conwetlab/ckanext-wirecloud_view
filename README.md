# CKAN WireCloud dashboards

[![Build Status](https://travis-ci.org/conwetlab/ckanext-wirecloud_view.svg?branch=develop)](https://travis-ci.org/conwetlab/ckanext-wirecloud_view)
[![Coverage Status](https://coveralls.io/repos/github/conwetlab/ckanext-wirecloud_view/badge.svg?branch=develop)](https://coveralls.io/github/conwetlab/ckanext-wirecloud_view?branch=develop)

CKAN view extension for the creation and display of resource data visualization dashboards through WireCloud embbeded dashboards.

With this extension you can create a view for a resource using WireCloud. You can set the view to load an existing dashboard or
create a custom dashboard from the view form.


## Requirements

You need the [Oauth2 extension](https://github.com/conwetlab/ckanext-oauth2) for CKAN in order to make this extension work.


## Installation

To install ckanext-wirecloud_view:

1. Activate your CKAN virtual environment, for example:

    ```
    . /usr/lib/ckan/default/bin/activate
    ```

2. Install the ckanext-wirecloudview Python package into your virtual environment:

    ```
    pip install ckanext-wirecloud_view
    ```

3. Add `wirecloud_view` to the `ckan.plugins` setting in your CKAN
   config file (e.g. `/etc/ckan/default/production.ini`).

4. Add proper values for the `ckan.wirecloud_view.url` and
   `ckan.wirecloud_view.editor_dashboard` settings in your CKAN config file:

    ```ini
    # URL of the WireCloud instance to use for creating the dashboards
    ckan.wirecloud_view.url = https://mashup.lab.fiware.org

    # ID of the dashboard/workspace to use for creating new visualization dashboards
    ckan.wirecloud_view.editor_dashboard = wirecloud/ckan-editor
    ```

5. Restart CKAN. For example if you've deployed CKAN with Apache:

    ```
    sudo service apache2 graceful
    ```

## Development Installation

To install ckanext-wirecloudview for development, activate your CKAN virtualenv and
do:

```
git clone https://github.com/conwetlab/ckanext-wirecloud_view.git
cd ckanext-wirecloud_view
python setup.py develop
```
