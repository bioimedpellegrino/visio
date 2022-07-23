#initDb.py

import sys
#import sqlitevisio_db
dbmgr_path= r'/home/pi/visio/apps/procedure/visiopackage'
sys.path.insert(1, dbmgr_path)
import djangosqlite_db
from djangosqlite_db import *

#create_knownface()

dbmgr=djangosqlite_db.Dbmgr()

'''
cameraname='camera1'
cameradesc= 'pi camera v.2'
insert_picamera(cameraname, cameradesc)

entname='entry1'
desc='porta1'
site='building1'
camera_id=1
insert_entity(entname, desc, site,camera_id)
'''
#ADD PERSONS
firstname="barack" 
lastname="obama" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/apps/pictures/portraits/" 
imagename="obama-240.jpg"
dbmgr.insert_person(firstname, lastname, birth_date, imagepath + imagename)

firstname="joe" 
lastname="biden" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/apps/pictures/portraits/" 
imagename="biden.jpg"
dbmgr.insert_person(firstname, lastname, birth_date, imagepath + imagename)

firstname="giorgio" 
lastname="peter" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/apps/pictures/portraits/" 
imagename="peter.jpg"
dbmgr.insert_person(firstname, lastname, birth_date, imagepath + imagename)


#conn.close()