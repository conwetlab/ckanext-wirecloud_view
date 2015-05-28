.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

=============
ckanext-wirecloudview
=============

CKAN view extension for the creation and display of resource data visualization dashboards through Wirecloud embbeded dashboards. 


------------
Requirements
------------

You need the [Oauth2 extension](https://github.com/conwetlab/ckanext-oauth2) for CKAN in order to make this extension work.


------------
Installation
------------

To install ckanext-wirecloud_view:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-wirecloudview Python package into your virtual environment::

     pip install ckanext-wirecloud_view

3. Add ``wirecloud_view`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

    # Wirecloud url    
    ckanext.wirecloud_view.url = https://yourwirecloudurl.com


------------------------
Development Installation
------------------------

To install ckanext-wirecloudview for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/billescas/ckanext-wirecloudview.git
    cd ckanext-wirecloudview
    python setup.py develop
    pip install -r dev-requirements.txt