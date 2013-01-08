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
    numberOfLinesToBeSkipped = 0 #235

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
                if(len(matcher.group(1)) > 0 or len(matcher.group(3)) > 0):
                    if(len(matcher.group(2)) > 0):
                        surname = matcher.group(1)
                        name = matcher.group(3)
                    else:
                        name = matcher.group(1) + matcher.group(3)
                        surname = ""
                outputFile.write(name + self.seperator + surname + self.seperator + matcher.group(5) + self.seperator + matcher.group(6) + self.seperator + matcher.group(7) + self.seperator + matcher.group(8) + self.seperator + matcher.group(9) + self.seperator + matcher.group(10) + self.seperator + matcher.group(11) + "\n")
            elif(len(line) == 1):
                continue
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
