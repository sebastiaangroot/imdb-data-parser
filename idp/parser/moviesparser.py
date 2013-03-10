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
from ..utils.filehandler import IMDBList
import logging
import re

class MoviesParser(BaseParser):
    """
    Parses movies.list dump

    RegExp: /((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\t+(.*)$/gm
    pattern: ((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\t+(.*)$
    flags: gm
    8 capturing groups:
        group 1: #TITLE (UNIQUE KEY)
        group 2: (.*? \(\S{4,}\))                    movie name + year
        group 3: (\(\S+\))                           type ex:(TV)
        group 4: (\{(.*?) ?(\(\S+?\))?\})            series info ex: {Ally Abroad (#3.1)}
        group 5: (.*?)                               episode name ex: Ally Abroad
        group 6: ((\(\S+?\))                         episode number ex: (#3.1)
        group 7: (\{\{SUSPENDED\}\})                 is suspended?
        group 8: (.*)                                year
    """

    # properties
    baseMatcherPattern = "((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\t+(.*)$"
    inputFileName = "movies.list"
    #FIXME: zafer: I think using a static number is critical for us. If imdb sends a new file with first 10 line fucked then we're also fucked
    numberOfLinesToBeSkipped = 15
    scripts = {
        'drop' : 'DROP TABLE IF EXISTS movies;\n',
        'create' : 'CREATE TABLE movies( id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(id), name VARCHAR(255), year INT );\n',
        'insert' : 'INSERT INTO movies(name, year) VALUES\n'
    }

    def __init__(self, preferencesMap):
        super(MoviesParser, self).__init__(preferencesMap)

    def parse_into_tsv(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            self.outputFile.write(matcher.group(1) + self.seperator + matcher.group(2) + self.seperator + matcher.group(3) + self.seperator + matcher.group(5) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + "\n")
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1

    def parse_into_db(self, matcher):
        isMatch = matcher.match(self.baseMatcherPattern)

        if(isMatch):
            self.sqlFile.write("(\"" + re.escape(matcher.group(1)) + "\", " + matcher.group(8) + "),\n")
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fuckedUpCount += 1
