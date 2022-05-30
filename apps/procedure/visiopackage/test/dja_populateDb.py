#initDb.py
#import sqlitevisio_db
from djangosqlite_db import *

#create_knownface()
#imagepath="/home/pi/visiog/pictures/portraits/"

dbman= Dbmgr()

def populateDB():
    facedetection=1
    facerecognition = 1
    facemotion_agegender = 1
    #faceagegender = 1
    saveimage = 1
    useaudio = 1
    framelapse = 0.04
    dbman.insert_param(facedetection, facerecognition, facemotion_agegender, saveimage, useaudio, framelapse)
    
    cameraname='camera1'
    desc= 'pi camera v.2'
    usersel='-'
    dbman.insert_picamera(cameraname, desc, usersel)
    #Dbmgr.insert_picamera(dbman, cameraname, desc, usersel)
    
    entname='entry1'
    desc='porta1'
    site='building1'
    camera_id=1
    dbman.insert_entity(entname, desc, site,camera_id)
    
    #ADD PERSONS
    firstname="barack" 
    lastname="obama" 
    #gender="male" 
    birth_date="" 
    document_num="" 
    img = "obama-240.jpg" #imagepath + "obama-240.jpg"
    #imagename="obama-240.jpg"
    dbman.insert_person(firstname, lastname, birth_date, img)
    
    firstname="joe" 
    lastname="biden" 
    #gender="male" 
    birth_date="" 
    document_num="" 
    img = "biden.jpg" #imagepath + "biden.jpg" 
    #imagename="biden.jpg"
    dbman.insert_person(firstname, lastname, birth_date, img)
    
    firstname="giorgio" 
    lastname="peter" 
    #gender="male" 
    birth_date="" 
    document_num="" 
    img = "peter.jpg" #imagepath + "peter.jpg"
    #imagename="peter.jpg"
    dbman.insert_person(firstname, lastname, birth_date, img)

#firstname="anonimous" 
#lastname="anonimous" 
#gender="male" 
#birth_date="" 
#document_num="" 
#img = "" #imagepath + "peter.jpg"
#imagename="peter.jpg"
#dbman.insert_person(firstname, lastname, birth_date, img)


#conn.close()