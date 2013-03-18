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

from .baseparser import *


class DirectorsParser(BaseParser):
    """
    RegExp: /(.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*\)|EDIT)?\s*(<.*>)?$/gm
    pattern: (.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*\)|EDIT)?\s*(<.*>)?$
    flags: gm
    10 capturing groups: 
        group 1: (.*?)                               surname, name                        
        group 2: #TITLE (UNIQUE KEY)
        group 3: (.*? \(\S{4,}\))                    movie name + year
        group 4: (\(\S+\))                           type ex:(TV)
        group 5: (\{(.*?) ?(\(\S+?\))?\})            series info ex: {Ally Abroad (#3.1)}
        group 6: (.*?)                               episode name ex: Ally Abroad
        group 7: (\(\S+?\))                          episode number ex: (#3.1)
        group 8: (\{\{SUSPENDED\}\})                 is suspended?
        group 9: (\(.*\))                            info
        group 10: ()
    """

    # properties
    base_matcher_pattern = '(.*?)\t+((.*? \(\S{4,}\)) ?(\(\S+\))? ?(?!\{\{SUSPENDED\}\})(\{(.*?) ?(\(\S+?\))?\})? ?(\{\{SUSPENDED\}\})?)\s*(\(.*\)|EDIT)?\s*(<.*>)?$'
    input_file_name = "directors.list"
    number_of_lines_to_be_skipped = 235
    db_table_info = {
        'tablename' : 'directors',
        'columns' : [
            {
                'colname' : '',
                'colinfo' : DbScriptHelper.keywords['string'] + '(255) NOT NULL'
            }
        ],
        'constraints' : ''
    }
    end_of_dump_delimiter = ""

    name = ""
    surname = ""

    def __init__(self, preferences_map):
        super(DirectorsParser, self).__init__(preferences_map)

    def parse_into_tsv(self, matcher):
        is_match = matcher.match(self.base_matcher_pattern)

        if(is_match):
            if(len(matcher.group(1).strip()) > 0):
                namelist = matcher.group(1).split(', ')
                if(len(namelist) == 2):
                    self.name = namelist[1]
                    self.surname = namelist[0]
                else:
                    self.name = namelist[0]
                    self.surname = ""

            self.tsv_file.write(self.name + self.seperator + self.surname + self.seperator + matcher.group(2) + self.seperator + matcher.group(3) + self.seperator + matcher.group(4) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + self.seperator + matcher.group(9) + "\n")
        elif(len(matcher.get_last_string()) == 1):
            pass
        else:
            logging.critical("This line is fucked up: " + matcher.get_last_string())
            self.fucked_up_count += 1

    def parse_into_db(self, matcher):
        #TODO
        pass
