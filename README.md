imdb-data-parser
================

Parses the IMDB dumps into CSV and Relational Database insert queries
Uses IMDB dumps from: http://www.imdb.com/interfaces

imdb-data-parser is a free software licensed by GPLv3.


Requirements
================
Python 3.x
python3-psycopg2

Configuring
================
All configuration data stays at `idp/settings.py.example`

You need to copy this file as `settings.py` and edit this file before running the project

    cd idp
    cp settings.py.example settings.py
    your_favourite_editor settings.py

Executing
---------

    ~/imdb-data-parser$ ./imdbparser.py

You can use -h parameter to see list of optional arguments

    ~/imdb-data-parser$ ./imdbparser.py -h
