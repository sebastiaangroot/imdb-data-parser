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
import logging

class DirectorsParser(BaseParser):
    """
    RegExp: /(.*?)(, )?(\S*)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)(\(.*\))?$/gm
    pattern: (.*?)(, )?(\S*)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)(\(.*\))?$
    flags: gm
    11 capturing groups: 
        group 1: (.*?)                               surname
        group 2: (, )                                just grouping ,
        group 3: (\S*)                               name
        group 4: #TITLE (UNIQUE KEY)
        group 5: (.*? \(\S{4,}\))                    movie name + year
        group 6: (\(\S+\))                           type ex:(TV)
        group 7: (\{(.*?) ?(\(\S+?\))?\})            series info ex: {Ally Abroad (#3.1)}
        group 8: (.*?)                               episode name ex: Ally Abroad
        group 9: (\(\S+?\))                          episode number ex: (#3.1)
        group 10: (\{\{SUSPENDED\}\})                is suspended?
        group 11: (\(.*\))                           info
    """
  
    # properties
    baseMatcherPattern = "(.*?)(, )?(\S*)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)(\(.*\))?$"
    inputFileName = "directors.list"
    numberOfLinesToBeSkipped = 235
    scripts = { #TODO: fill 
        'drop' : '',
        'create' : '',
        'insert' : ''
    }

    def __init__(self, preferencesMap):
        self.mode = preferencesMap['mode']

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            if(len(matcher.group(1)) > 0 or len(matcher.group(3)) > 0):
                if(len(matcher.group(2)) > 0):
                    surname = matcher.group(1)
                    name = matcher.group(3)
                else:
                    name = matcher.group(1) + matcher.group(3)
                    surname = ""
                    
                self.outputFile.write(name + self.seperator + surname + self.seperator + matcher.group(5) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + self.seperator + matcher.group(9) + self.seperator + matcher.group(10) + self.seperator + matcher.group(11) + "\n")
        elif(len(matcher.get_last_string()) == 1):
            pass
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1

    def parse_into_db(self, matcher):
        #TODO
        pass
