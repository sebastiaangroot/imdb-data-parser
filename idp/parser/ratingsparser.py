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

class RatingsParser(BaseParser):
    """
    RegExp: /\s*(\S*)\s*(\S*)\s*(\S*)\s*((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)$/gm
    pattern: \s*(\S*)\s*(\S*)\s*(\S*)\s*((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)$
    flags: gm
    10 capturing groups:
        group 1: (\S*)                               distribution
        group 2: (\S*)                               votes
        group 3: (\S*)                               rank
        group 4: #TITLE (UNIQUE KEY)
        group 5: (.*? \(\S{4,}\))                    movie name + year
        group 6: (\(.+\))                            type ex:(TV)
        group 7: (\{(.*?)\s?(\(.+?\))\})             series info ex: {Ally Abroad (#3.1)}
        group 8: (.*?)                               episode name ex: Ally Abroad
        group 9: (\(.+?\))                           episode number ex: (#3.1)
        group 10: (\{\{SUSPENDED\}\})                is suspended?
    """
  
    # properties
    baseMatcherPattern = "\s*(\S*)\s*(\S*)\s*(\S*)\s*((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)$"
    inputFileName = "ratings.list"
    numberOfLinesToBeSkipped = 28
    scripts = { #TODO: fill 
        'drop' : '',
        'create' : '',
        'insert' : ''
    }

    def __init__(self, preferencesMap):
        super(RatingsParser, self).__init__(preferencesMap)

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            self.outputFile.write(matcher.group(1) + self.seperator + matcher.group(2) + self.seperator + matcher.group(3) + self.seperator + matcher.group(4) + self.seperator + matcher.group(5) + self.seperator + matcher.group(6) + self.seperator + matcher.group(8) + self.seperator + matcher.group(8) + self.seperator + matcher.group(9) + self.seperator + matcher.group(10) + "\n")
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1

    def parse_into_db(self, matcher):
        #TODO
        pass
