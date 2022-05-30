#add_person_entity.py
#import sqlitevisio_db

#tutti i file .py della cartella visiopackage sono in package
import sys
sys.path.append("/home/pi/visio/visiopackage/sqlite")
from sqlitevisio_db import *

#
import os.path
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
dbfullpath=os.path.join(BASE_DIR,"../../data/visio.sqlite3")

#dbfullpath= r'/home/pi/visio/data/visio.sqlite3'
create_person_entity(dbfullpath)
