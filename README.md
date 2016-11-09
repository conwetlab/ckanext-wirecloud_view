# CKAN WireCloud dashboards

CKAN view extension for the creation and display of resource data visualization dashboards through WireCloud embbeded dashboards.

With this extension you can create a view for a resource using WireCloud. You can set the view to load an existing mashup or
create your own mashup directly from the editing view page in CKAN.


## Requirements

You need the [Oauth2 extension](https://github.com/conwetlab/ckanext-oauth2) for CKAN in order to make this extension work.


## Installation

To install ckanext-wirecloud_view:

1. Activate your CKAN virtual environment, for example:

    ```
    . /usr/lib/ckan/default/bin/activate
    ```

2. Install the ckanext-wirecloudview Python package into your virtual environment::

    ```
    pip install ckanext-wirecloud_view
    ```

3. Add `wirecloud_view` to the `ckan.plugins` setting in your CKAN
   config file (e.g. `/etc/ckan/default/production.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache:

    ```
    sudo service apache2 graceful
    ```

## Config Settings

Before using this extension you must set the next variables in your CKAN config file
(`production.ini` or `development.ini`):

```ini
# WireCloud URL: the URL of the WireCloud instance
ckan.wirecloud_view.url = https://yourwirecloudurl.com

# Editor URL: the URL of the workspace that works
# as an editor for creating new mashups
ckan.wirecloud_view.editor_url = https://yourwirecloudurl.com/YourUser/YourEditorWorkspace
```

## Development Installation

To install ckanext-wirecloudview for development, activate your CKAN virtualenv and
do:

```
git clone https://github.com/conwetlab/ckanext-wirecloud_view.git
cd ckanext-wirecloud_view
python setup.py develop
```
