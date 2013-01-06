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

from ..settings import *
from ftplib import FTP
import gzip
from .filehandler import *
import logging

def download():
    logging.info("lists will downloaded from server:" + INTERFACES_SERVER)

    ftp = FTP(INTERFACES_SERVER)
    ftp.login()
    download_count = 0
    for list in LISTS:
        try:
            logging.info("started to download list:" + list)
            r = ftp.retrbinary('RETR '+INTERFACES_DIRECTORY+list+'.list.gz',
                open(SOURCE_PATH+list+'.list.gz', 'wb').write)
            logging.info(list + "list downloaded successfully")
            download_count = download_count+1
            extract(get_full_path(list+".list", True))
        except Exception as e:
            print("ERROR: there is a problem when downloading list " + list + "\n\t" + str(e))
    logging.info(str(download_count) + " lists are downloaded")
    ftp.quit()