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

from abc import *
from ..utils.filehandler import *

class BaseParser(metaclass=ABCMeta):
    """Common methods for all parser classes"""

    seperator = "\t"

    @abstractmethod
    def parse_into_tsv(self):
        raise NotImplemented

    @abstractmethod
    def parse_into_db(self):
        raise NotImplemented

    def start_processing(self):
        if(self.preferencesMap["mode"] == "TSV"):
            self.parse_into_tsv()
        elif(self.preferencesMap["mode"] == "SQL"):
            self.parse_into_db()
        else:
            raise NotImplemented("Mode: " + self.preferencesMap["mode"])

    def get_input_file(self):
        return openfile(get_full_path(self.inputFileName))

    def get_output_file(self):
        return open(get_full_path_for_tsv(self.inputFileName), "w")

    @abstractproperty
    def baseMatcherPattern(self):
        raise NotImplemented

    @abstractproperty
    def inputFileName(self):
        raise NotImplemented

    @abstractproperty
    def numberOfLinesToBeSkipped(self):
        raise NotImplemented

    @abstractproperty
    def preferencesMap(self):
        raise NotImplemented