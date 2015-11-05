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

import sqlalchemy as sa

Dashboard = None


def init_db(model):

    global Dashboard
    if Dashboard is None:

        class _Dashboard(model.DomainObject):

            @classmethod
            def by_resource_and_view(cls, resource_id, view_id):
                return model.Session.query(cls).filter_by(resource_id=resource_id, view_id=view_id).first()

        Dashboard = _Dashboard

        dashboard_table = sa.Table('wirecloud_dashboard', model.meta.metadata,
            sa.Column('view_id', sa.types.UnicodeText, primary_key=True),
            sa.Column('resource_id', sa.types.UnicodeText, primary_key=True),
            sa.Column('dashboard_path', sa.types.UnicodeText)
        )

        # Create the table only if it does not exist
        dashboard_table.create(checkfirst=True)

        model.meta.mapper(Dashboard, dashboard_table)