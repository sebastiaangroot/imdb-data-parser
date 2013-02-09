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
    RegExp: /((.+?) (.*))|\n/g
    pattern: ((.+?) (.*))|\n
    flags: g
    2 capturing groups: 
       group 1: (.+?)   type of the line
       group 2: (.*)    if the line-type is - then this line is plot, not the whole but one line of it
                        if the line-type is # then this line is movie
    """
  
    # properties
    baseMatcherPattern = "((.+?) (.*))|\n"
    inputFileName = "trivia.list"
    numberOfLinesToBeSkipped = 15
    scripts = { #TODO: fill 
        'drop' : '',
        'create' : '',
        'insert' : ''
    }
    
    title = ""
    trivia = ""

    def __init__(self, preferencesMap):
        self.mode = preferencesMap['mode']
        self.list = IMDBList(self.inputFileName, preferencesMap)
        self.inputFile = self.list.get_input_file()
        self.outputFile = self.list.get_output_file()

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            if(matcher.group(2) == "#"): #Title
                self.title = matcher.group(3)
            elif(matcher.group(2) == "-"): #Descriptive text
                self.trivia = matcher.group(3)
            elif(matcher.group(2) == " "):
                self.trivia += ' ' + matcher.group(3)
            else:
                self.outputFile.write(self.title + self.seperator + self.trivia + "\n")
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1

    def parse_into_db(self, matcher):
        #TODO
        pass
