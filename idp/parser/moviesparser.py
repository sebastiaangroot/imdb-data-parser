from .baseparser import BaseParser
from ..utils.regexhelper import *
import logging

class MoviesParser(BaseParser):
    """
    RegExp: /((.*? \(\S{4,}\))\s?(\(.+\))?\s?(\{(.*?)\s?(\(.+?\))\})?\s?(\{\{SUSPENDED\}\})?)\s*(.*$)/gm
    pattern: ((.*? \(\S{4,}\))\s?(\(.+\))?\s?(\{(.*?)\s?(\(.+?\))\})?\s?(\{\{SUSPENDED\}\})?)\s*(.*$)
    flags: gm
    6 capturing groups: 
        group 1: #TITLE (UNIQUE KEY)
        group 2: (.*? \(\S{4,}\))                    movie name + year
        group 3: (\(.+\))                            type ex:(TV)
        group 4: (\{(.*?)\s?(\(.+?\))\})             series info ex: {Ally Abroad (#3.1)}
        group 5: (.*?)                               episode name ex: Ally Abroad
        group 6: (\(.+?\))                           episode number ex: (#3.1)
        group 7: (\{\{SUSPENDED\}\})                 is suspended?
        group 8: (.*$)                               year
    """
  
    # properties
    baseMatcherPattern = "((.*? \(\S{4,}\))\s?(\(.+\))?\s?(\{(.*?)\s?(\(.+?\))\})?\s?(\{\{SUSPENDED\}\})?)\s*(.*$)"
    inputFileName = "movies.list"
    numberOfLinesToBeSkipped = 15

    def __init__(self, preferencesMap):
        self._preferencesMap = preferencesMap

    @property
    def preferencesMap(self):
        return self._preferencesMap

    def parse_into_tsv(self):
        import time

        startTime = time.time()

        inputFile = self.get_input_file()
        outputFile = self.get_output_file()
        counter = 0
        fuckedUpCount = 0
        numberOfProcessedLines = 0

        for line in inputFile :
          if(numberOfProcessedLines > self.numberOfLinesToBeSkipped):
            matcher = RegExHelper(line)
            isMatch = matcher.match(self.baseMatcherPattern)

            if(isMatch):
                outputFile.write(matcher.group(1).strip() + self.seperator + matcher.group(2) + self.seperator + matcher.group(3) + self.seperator + matcher.group(5) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + "\n")
            else:
                logging.critical("This line is fucked up: " + line)
                fuckedUpCount += 1
          numberOfProcessedLines +=  1

        outputFile.flush()
        outputFile.close()
        inputFile .close()

        logging.info("Finished with " + str(fuckedUpCount) + " fucked up line\n")
        logging.info("Duration: " + str(round(time.time() - startTime)))

    def parse_into_db(self):
        #TODO
        pass
