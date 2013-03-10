#!/usr/bin/env python3

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

"""
Dealing with ": No such file or directory" error:
http://stackoverflow.com/a/8735625/878361
"""

import sys
import argparse
import logging
from idp.utils.loggerinitializer import *
from idp.parser.parsinghelper import ParsingHelper
from idp.settings import *
import datetime

# check python version
if sys.version_info.major != 3:
    sys.exit("Error: wrong version! You need to install python3 to run this application properly.")

parser = argparse.ArgumentParser(description="an IMDB data parser")
parser.add_argument('-m', '--mode', help='Parsing mode, defines output of parsing process. Default: CSV', choices=['TSV', 'SQL', 'DB'])
parser.add_argument('-i', '--input_dir', help='source directory of interface lists')
parser.add_argument('-o', '--output_dir', help='destination directory for outputs')
parser.add_argument('-u', '--update_lists', action='store_true', help='downloads lists from server')

args = parser.parse_args()

# preparing preferences map
if args.mode:
    mode = args.mode
else: #default
    mode = "TSV"

if args.input_dir:
    inputDir = args.input_dir
else:
    inputDir = INPUT_DIR

postfix =  datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + '_ImdbParserOutput'
if args.input_dir:
    outputDir = os.path.join(args.output_dir, postfix)
else:
    outputDir = os.path.join(OUTPUT_DIR, postfix)

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

preferencesMap = {
    "mode":mode,
    "inputDir": inputDir,
    "outputDir": outputDir
}

initialize_logger(preferencesMap)

logging.info("mode:%s", mode)
logging.info("input_dir:%s", inputDir)
logging.info("output_dir:%s", outputDir)
logging.info("update_lists:%s", args.update_lists)

if args.update_lists:
    from idp.utils import listdownloader
    logging.info("Downloading IMDB dumps, this may take a while depending on your connection speed")
    listdownloader.download()

logging.info("Parsing, please wait. This may take very long time...")

ParsingHelper.parse_all(preferencesMap)

print ("All done, enjoy ;)")
