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

import gzip
import os.path
from ..settings import *
import logging

class IMDBList(object):
    def __init__(self, listname):
        #TODO: check listname finishes with .list
        self.listname = listname

        fullFilePath = os.path.join(INPUT_DIR, self.listname)
        print(fullFilePath)
        logging.info("Trying to find file: %s", fullFilePath)
        if os.path.isfile(fullFilePath):
            logging.info("File found: %s", fullFilePath)
            self.file = open(fullFilePath, "r", encoding='iso-8859-1')
        else:
            logging.error("File cannot be found: %s", fullFilePath)

    def full_path(self):
        if self.listname.lower().endswith(".gz"):
            return os.path.join(INPUT_DIR, self.listname) + ".gz"
        return os.path.join(INPUT_DIR, self.listname)

    def tsv_path(self):
        return self.full_path() + ".tsv"

def get_full_path(filename, isCompressed = False):
    """
    constructs a full path for a dump file in the INPUT_DIR
    filename should be without '.list'
    """
    if(isCompressed):
        return os.path.join(INPUT_DIR, filename) + ".gz"
    else:
        return os.path.join(INPUT_DIR, filename)

def get_full_path_for_tsv(filename):
    return get_full_path(filename) + ".tsv"

def get_decompressed_file_name(fullpath):
    return fullpath[:-3]

def extract(fullpath):
    try:
        logging.info('started to extract list: %s', fullpath)
        with gzip.open(fullpath, 'rb') as f:
            file_content = f.read()
        listfile = open(get_decompressed_file_name(fullpath), 'wb')
        listfile.write(file_content)
        listfile.close()
        logging.info(fullpath + ' list extracted successfully')
    except Exception as e:
        logging.error('error when extracting list: ' + fullpath + "\n\t" + str(e))
        return 1
    return 0

def openfile(fullFilePath):

    logging.info("Trying to find file: %s", fullFilePath)
    if os.path.isfile(fullFilePath):
        logging.info("File found: %s", fullFilePath)
        return open(fullFilePath, "r", encoding='iso-8859-1')

    logging.error("File cannot be found: %s", fullFilePath)

#
#this part removed until python 3.3 becomes available for ubuntu LTS and debian
#
#   print("Trying to find file:", fullFilePath)
#   if os.path.isfile(fullFilePath):
#       print("File found:", fullFilePath)
#       return gzip.open(fullFilePath, 'rt')
#   print("File cannot be found:", fullFilePath)

    logging.info("Trying to find file: %s", fullFilePath + ".gz")
    if os.path.isfile(fullFilePath + ".gz"):
        logging.info("File found: %s", fullFilePath + ".gz")
        if extract(fullFilePath + ".gz") == 0:
            return open(fullFilePath, "r", encoding='iso-8859-1')
        else:
            raise RuntimeError("Unknown error occured")
    logging.error("File cannot be found: %s", fullFilePath + ".gz")

    raise RuntimeError("FileNotFoundError: " + fullFilePath)

if __name__ == "__main__":
    f = IMDBList("movies.list")
    print(f.full_path())
    print(f.tsv_path())