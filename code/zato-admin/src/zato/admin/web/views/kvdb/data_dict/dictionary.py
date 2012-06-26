# -*- coding: utf-8 -*-

"""
Copyright (C) 2012 Dariusz Suchojad <dsuch at gefira.pl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import logging

# Zato
from zato.admin.web.forms.kvdb.data_dict.dictionary import CreateForm, EditForm
from zato.admin.web.views import CreateEdit, Delete as _Delete, Index as _Index

logger = logging.getLogger(__name__)

class DictItem(object):
    def __init__(self, system, name, value):
        self.system = system
        self.name = name
        self.value = value

class Index(_Index):
    meth_allowed = 'GET'
    url_name = 'kvdb-data-dict-dictionary'
    template = 'zato/kvdb/data_dict/dictionary.html'
    
    soap_action = 'zato:kvdb.data-dict.dictionary.get-list'
    output_class = DictItem
    
    class SimpleIO(_Index.SimpleIO):
        output_required = ('name', 'source_system', 'target_system', 'source_name', 'target_name', 'source_value', 'target_value')
        output_repeated = True

    def handle(self):
        return {
            'create_form': CreateForm(),
            'edit_form': EditForm(prefix='edit'),
        }

class _CreateEdit(CreateEdit):
    meth_allowed = 'POST'
    class SimpleIO(CreateEdit.SimpleIO):
        input_required = ('name', 'is_active', 'host', 'user', 'timeout', 'acct', 'port', 'dircache')
        output_required = ('id', 'name')
        
    def success_message(self, item):
        return 'Successfully {0} the dictionary [{1}]'.format(self.verb, item.name.text)

class Create(_CreateEdit):
    url_name = 'kvdb-data-dict-dictionary-create'
    soap_action = 'zato:kvdb.data-dict.dictionary.create'

class Edit(_CreateEdit):
    url_name = 'kvdb-data-dict-dictionary-edit'
    form_prefix = 'edit-'
    soap_action = 'zato:kvdb.data-dict.dictionary.edit'

class Delete(_Delete):
    url_name = 'kvdb-data-dict-dictionary-delete'
    error_message = 'Could not delete the data dictionary'
    soap_action = 'zato:kvdb.data-dict.dictionary.delete'
