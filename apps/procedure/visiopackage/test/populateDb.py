#initDb.py
#import sqlitevisio_db
from sqlitevisio_db import *

#create_knownface()


cameraname='camera1'
cameradesc= 'pi camera v.2'
insert_picamera(cameraname, cameradesc)

entname='entry1'
desc='porta1'
site='building1'
camera_id=1
insert_entity(entname, desc, site,camera_id)

#ADD PERSONS
firstname="barack" 
lastname="obama" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/pictures/portraits/" 
imagename="obama-240.jpg"
insert_person(firstname, lastname, gender, birth_date, document_num, imagepath, imagename)

firstname="joe" 
lastname="biden" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/pictures/portraits/" 
imagename="biden.jpg"
insert_person(firstname, lastname, gender, birth_date, document_num, imagepath, imagename)

firstname="giorgio" 
lastname="peter" 
gender="male" 
birth_date="" 
document_num="" 
imagepath="/home/pi/visio/pictures/portraits/" 
imagename="peter.jpg"
insert_person(firstname, lastname, gender, birth_date, document_num, imagepath, imagename)


#conn.close()