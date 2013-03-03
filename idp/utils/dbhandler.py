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

import psycopg2
import logging

class DB(object):
    def __init__(self, dbsettings):
        self.conn = psycopg2.connect("hostaddr="+dbsettings['DBHOST']+" user="+dbsettings['DBUSER']+" password="+dbsettings['DBPASSWORD']+" dbname="+dbsettings['DBNAME']+" connect_timeout=10")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name, create_query):
        try:
            logging.info("query is "+create_query)
            self.cur.execute("DROP TABLE IF EXISTS "+table_name)
            logging.info("dropped table "+table_name)
            self.cur.execute(create_query)
            self.conn.commit()
            logging.info("committed changes to db")
        except Exception as e:
            logging.error("db creation error: %s", e)

    def insert(self, table_name, data_dict):
        try:
            query = "INSERT INTO "+table_name+"("+", ".join(data_dict.keys())+") VALUES ("+", ".join(['%s']*len(data_dict.keys()))+")"
            self.cur.execute(query, list(data_dict.values()))
            self.conn.commit()
        except Exception as e:
            logging.error("db insertion error: %s", e)
