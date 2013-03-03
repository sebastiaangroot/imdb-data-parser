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

import unittest
import psycopg2
from idp.utils import dbhandler
from idp import settings

class DBTests(unittest.TestCase):
    def setUp(self):
        dbsettings={'DBHOST': settings.DBHOST, 'DBUSER': settings.DBUSER, 'DBPASSWORD': settings.DBPASSWORD, 'DBNAME': settings.DBNAME}
        self.db = dbhandler.DB(dbsettings)
        self.conn = psycopg2.connect("hostaddr="+dbsettings['DBHOST']+" user="+dbsettings['DBUSER']+" password="+dbsettings['DBPASSWORD']+" dbname="+dbsettings['DBNAME']+" connect_timeout=10")
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_create_table(self):
        self.cur.execute("DROP TABLE IF EXISTS test")
        self.conn.commit()
        self.db.create_table('test', "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        self.cur.execute("SELECT * FROM pg_catalog.pg_tables where tablename='test'")
        self.assertEqual(1, self.cur.rowcount)

    def test_insert_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS unittest(id serial PRIMARY KEY, num integer, data varchar);")
        self.conn.commit()
        self.cur.execute("select * from unittest")
        before=self.cur.rowcount
        values={'num':12, 'data':'hede'}
        self.db.insert("unittest", values)
        self.cur.execute("select * from unittest")
        after=self.cur.rowcount
        self.assertEqual(before+1, after)

if __name__ == '__main__':
    unittest.main()
