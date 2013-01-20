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

class ActressesParser(BaseParser):
    """
    RegExp: /(.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*?\))?\s*(\(.*\))?\s*(\[.*\])?\s*(<.*>)?$/gm
    pattern: (.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*?\))?\s*(\(.*\))?\s*(\[.*\])?\s*(<.*>)?$
    flags: gm
    12 capturing groups: 
        group 1: (.*?)                               surname, name                        
        group 2: #TITLE (UNIQUE KEY)
        group 3: (.*? \(\S{4,}\))                    movie name + year
        group 4: (\(\S+\))                           type ex:(TV)
        group 5: (\{(.*?) ?(\(\S+?\))?\})            series info ex: {Ally Abroad (#3.1)}
        group 6: (.*?)                               episode name ex: Ally Abroad
        group 7: (\(\S+?\))                          episode number ex: (#3.1)
        group 8: (\{\{SUSPENDED\}\})                 is suspended?
        group 9: (\(.*?\))                           info 1
        group 10: (\(.*\))                           info 2
        group 11: (\[.*\])                           role
        group 12: ()
    """
  
    # properties
    baseMatcherPattern = '(.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*?\))?\s*(\(.*\))?\s*(\[.*\])?\s*(<.*>)?$'
    inputFileName = "actresses.list"
    numberOfLinesToBeSkipped = 241
    scripts = { #TODO: fill 
        'drop' : '',
        'create' : '',
        'insert' : ''
    }

    name = ""
    surname = ""

    def __init__(self, preferencesMap):
        self.mode = preferencesMap['mode']
        self.list = IMDBList(self.inputFileName, preferencesMap)
        self.inputFile = self.list.get_input_file()
        self.outputFile = self.list.get_output_file()

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            if(len(matcher.group(1).strip()) > 0):
                namelist = matcher.group(1).split(', ')
                if(len(namelist) == 2):
                    self.name = namelist[1]
                    self.surname = namelist[0]
                else:
                    self.name = namelist[0]
                    self.surname = ""
                    
            self.outputFile.write(self.name + self.seperator + self.surname + self.seperator + matcher.group(2) + self.seperator + matcher.group(3) + self.seperator + matcher.group(4) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + self.seperator + matcher.group(9) + self.seperator + matcher.group(10) + self.seperator + matcher.group(11) + "\n")
        elif(len(matcher.get_last_string()) == 1):
            pass
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1

    def parse_into_db(self, matcher):
        #TODO
        pass
