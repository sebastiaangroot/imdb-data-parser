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
from ..utils.decorators import durationLogged

class BaseParser(metaclass=ABCMeta):
    """
    Base class for all parser classes

    This class holds common methods for all parser classes and
    must be implemented by any Parser class

    Implementing classes' responsibilities are as follows:
    * Implement parse_into_tsv function
    * Implement parse_into_db function
    * Calculate fuckedUpCount and store in self.fuckedUpCount
    * Define following properties:
        - baseMatcherPattern
        - inputFileName
        - numberOfLinesToBeSkipped
        - scripts
    """

    seperator = "\t" #TODO: get from settings

    def __init__(self, preferencesMap):
        self.mode = preferencesMap['mode']
        self.list = IMDBList(self.inputFileName, preferencesMap)
        self.inputFile = self.list.get_input_file()
        if (self.mode == "TSV"):
          self.outputFile = self.list.get_output_file()
        elif (self.mode == "SQL"):
          self.sqlFile = self.list.get_sql_file()
          self.sqlFile.write(self.scripts['drop'])
          self.sqlFile.write(self.scripts['create'])
          self.sqlFile.write(self.scripts['insert'])

    @abstractmethod
    def parse_into_tsv(self, matcher):
        raise NotImplemented

    @abstractmethod
    def parse_into_db(self, matcher):
        raise NotImplemented

    @durationLogged
    def start_processing(self):
        '''
        Actual parsing and generation of scripts (tsv & sql) are done here.
        '''

        if(self.mode == "TSV"):
            pass
        elif(self.mode == "SQL"):
            pass

        self.fuckedUpCount = 0
        counter = 0
        numberOfProcessedLines = 0

        for line in self.inputFile : #assuming the file is opened in the subclass before here
            if(numberOfProcessedLines >= self.numberOfLinesToBeSkipped):
                #end of data
                #TODO: get from subclass, assume '-----------' as default
                if("--------------" in line):
                    break

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
        logging.info("Finished with " + str(self.fuckedUpCount) + " fucked up line")

    ##### Below methods force associated properties to be defined in any derived class #####

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
