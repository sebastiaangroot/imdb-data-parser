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

from .baseparser import BaseParser
from ..utils.regexhelper import *
from ..utils.filehandler import IMDBList
import logging

class TriviaParser(BaseParser):
    """
    RegExp: #TODO
    pattern: 
    flags: g
        capturing groups: 
    """
  
    # properties
    baseMatcherPattern = ""
    inputFileName = "trivia.list"
    numberOfLinesToBeSkipped = 15
    scripts = { #TODO: fill 
        'drop' : '',
        'create' : '',
        'insert' : ''
    }

    def __init__(self, preferencesMap):
        self.mode = preferencesMap['mode']
        self.list = IMDBList(self.inputFileName, preferencesMap)
        self.inputFile = self.list.get_input_file()
        self.outputFile = self.list.get_output_file()

        # specific to this class
        self.title = ""
        self.plot = ""

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            #TODO

    def parse_into_db(self, matcher):
        #TODO
        pass
