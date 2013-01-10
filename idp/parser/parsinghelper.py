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

from idp import settings
import logging
import traceback

class ParsingHelper(object):
    """ParsingHelper manages parsing order"""

    @staticmethod
    def parse_all(preferencesMap):

        def get_parser_class_for( itemName ):
            """
            Thanks to http://stackoverflow.com/a/452981
            """
            kls = "idp.parser." + itemName + "parser." + itemName.title() + "Parser"
            parts = kls.split('.')
            module = ".".join(parts[:-1])
            m = __import__( module )
            for comp in parts[1:]:
                m = getattr(m, comp)            
            return m

        for item in settings.LISTS:
            try:
                ParserClass = get_parser_class_for(item)
            except Exception as e:
                logging.error("No parser found for: " + item + "\n\tException is: " + str(e))
                continue
            logging.info("Parsing " + item + "...")
            parser = ParserClass(preferencesMap)
            try:
                parser.start_processing()
            except Exception as e:
                logging.error("Exception occured while parsing item: " + item + "\n\tException is: " + str(e))
                traceback.print_exc()
        logging.info("Parsing finished.")