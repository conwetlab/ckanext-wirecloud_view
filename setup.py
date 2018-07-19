#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012-2016 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from codecs import open
import os

import ckanext.wirecloudview


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ckanext-wirecloud_view',
    version=ckanext.wirecloudview.__version__,
    description='Provide visualization dashboards on CKAN using WireCloud',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/conwetlab/ckanext-wirecloud_view',
    author='CoNWeT Lab',
    author_email='wirecloud@conwet.com',
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='CKAN dashboard data visualization WireCloud',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'ckanext-oauth2>=0.4.0',
        'six',
    ],
    include_package_data=True,
    package_data={},
    data_files=[],
    entry_points='''
        [ckan.plugins]
        wirecloud_view=ckanext.wirecloudview.plugin:WirecloudView
    ''',
)
