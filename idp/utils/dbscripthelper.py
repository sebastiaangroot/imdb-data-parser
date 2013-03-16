"""
This file is part of imdb-data-parser.

imdb-data-parser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

imdb-data-parser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with imdb-data-parser.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

class DbScriptHelper(object):
    keywords = {
        'string' : 'VARCHAR2',
        'number' : 'NUMBER',
        'date' : 'DATE'
    }

    scripts = {
        'drop' : 'DROP TABLE ',
        'create' : 'CREATE TABLE ',
        'insert' : 'INSERT INTO '
    }

    def __init__(self, dbtableinfo):
        self.scripts['drop'] += dbtableinfo['tablename'] + ';' + os.linesep
        self.scripts['create'] += dbtableinfo['tablename'] + '(' + ', '.join(filter(None, (', '.join('%s %s' % (col['colname'], col['colinfo']) for col in dbtableinfo['columns']), dbtableinfo['constraints']))) + ') CHARACTER SET utf8 COLLATE utf8_bin;' + os.linesep
        self.scripts['insert'] += dbtableinfo['tablename'] + '(' + ', '.join(col['colname'] for col in dbtableinfo['columns']) + ') VALUES' + os.linesep