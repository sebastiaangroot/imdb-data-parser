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
from ..utils.regexhelper import *

class BaseParser(metaclass=ABCMeta):
    """Common methods for all parser classes"""

    seperator = "\t" #TODO: get from settings

    @abstractmethod
    def parse_into_tsv(self, matcher):
        raise NotImplemented

    @abstractmethod
    def parse_into_db(self, matcher):
        raise NotImplemented

    def start_processing(self):
        import time

        startTime = time.time()

        if(self.mode == "TSV"):
            #self.outputFile = self.get_output_file()
            pass
        elif(self.mode == "SQL"):
            pass
            #TODO: drop table if exists
            #TODO: create table
            # databaseHelper = DatabaseHelper()
            # databaseHelper.execute("")

        self.fuckedUpCount = 0
        counter = 0
        numberOfProcessedLines = 0

        for line in self.inputFile :
            if(numberOfProcessedLines >= self.numberOfLinesToBeSkipped):
                matcher = RegExHelper(line)

                if(self.mode == "TSV"):
                    '''
                    give the matcher directly to implementing class
                     and let it decide what to do when regEx is matched and unmatched
                    '''
                    self.parse_into_tsv(matcher)
                elif(self.mode == "SQL"):
                    self.parse_into_db(matcher)
                else:
                    raise NotImplemented("Mode: " + self.mode)

            numberOfProcessedLines +=  1

        self.inputFile.close()

        if 'outputFile' in locals():
            self.outputFile.flush()
            self.outputFile.close()

        if 'databaseHelper' in locals():
            databaseHelper.commit()
            databaseHelper.close()

        # fuckedUpCount is calculated in implementing class
        logging.info("Finished with " + str(self.fuckedUpCount) + " fucked up line\n")
        logging.info("Duration: " + str(round(time.time() - startTime)))

    # Below methods force associated properties to be defined in any derived class

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
    def scripts(self):
        raise NotImplemented
