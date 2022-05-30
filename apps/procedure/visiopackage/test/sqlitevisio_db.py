# sqlitevisio_db.py
#create folder /home/pi/lab/visio
#mkdir /home/pi/visio

#NB: posizione foreign key in create table deve essere sempre dopo ultima colonna!!!

#Give permission for user to folders visio/
#sudo chown -R pi visio/

#_name_=sqlitevisio_db

import pandas as pd 
import sqlite3
from datetime import datetime

# create DB 
dbpath= r'/home/pi/visiog/data/db.sqlite3'
conn = sqlite3.connect(dbpath)
#print(type(conn))
print('conn connected')

#t_camera(id, name, desc, timestamp);
#es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)
def create_camera():
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS home_camera (id INTEGER PRIMARY KEY, name TEXT, desc TEXT, 
                                                          user_selection TEXT);""")
    except:
        pass
    c.close()

#t_entity(id, name, desc, localita, camera_id, FOREIGN KEY(camera_id));
#può essere un'entrata, un corridoio o un oggetto/evento esposto
def create_entity():
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS home_entity (id INTEGER PRIMARY KEY, 
                                                             name TEXT, desc TEXT, site TEXT, 
                                                             camera INTEGER, 
                                                             FOREIGN KEY(camera) REFERENCES home_camera(id));""")
    except:
        pass
    c.close()

#t_imagedata(id, face_num,  timestamp, entity_id, FOREIGN KEY(entity_id));
#storage di face detection, ad ogni immagine di un'entita associo il numero di facce rilevate
def create_imagedata():
    c = conn.cursor()
    try: #image=imagefullpath
        c.execute("""CREATE TABLE IF NOT EXISTS home_imagedata (id INTEGER PRIMARY KEY, 
                                                                face_num INTEGER,  
                                                                created DATETIME DEFAULT CURRENT_TIMESTAMP, 
                                                                modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                                                                image TEXT, 
                                                                entity INTEGER, 
                                                                FOREIGN KEY(entity) REFERENCES home_entity(id));""")
    except:
        pass
    c.close()

#t_person(id, firstname,  lastname, gender, birth_date, document_num, imagepath, imagename);
# possono essere persone note con ritratti da confrontare per face recognition oppure 
#nel caso di interesse per sola analisi di (emotion, age, gender) senza face recognition e in riferimento ad un'entity
# "unknown"+counter come firstname
def create_person():
    c = conn.cursor()
    try: #document_num TEXT,
        c.execute("""CREATE TABLE IF NOT EXISTS home_person (id INTEGER PRIMARY KEY, 
                                                             firstname TEXT,  lastname TEXT, 
                                                             birth_date DATETIME,  
                                                             face_image TEXT);""") #imagefullpath
    except Exception as e:
        print(e)
        pass
    c.close()

#possibile classificazione emotions: happy, sad, fear, anger, surprise, neutral, disgust
#t_person_entity(person_id, entity_id, emotion, emotionval, timestamp);
# possono essere persone riconosciute per quella entita in un dato momento (=timestamp di t_imagedata)

def create_visiorecognition(fullpathdb):
    dbpath= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
    conn1 = sqlite3.connect(dbpath)
    print('db connected pers_ent')
    cu = conn1.cursor()
    try:
        cu.execute("""CREATE TABLE IF NOT EXISTS home_visiorecognition(id INTEGER PRIMARY KEY, 
                                                    person INTEGER not null, entity INTEGER not null,
                                                    age REAL, 
                                                    gender TEXT,
                                                    emotion TEXT,
                                                    foreign key(person) references home_person(id) on delete cascade,
                                                    FOREIGN KEY(entity) REFERENCES home_entity(id) on delete cascade);""")
    except Exception as e:
        print(e)
        pass
    conn1.commit()
    cu.close()
    conn1.close()


# es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)     
def insert_picamera(namein, cameradesc):
    #dbpath= r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO home_camera (name, desc, user_selection) values(?, ?,?)""",(namein,cameradesc,''))
    conn.commit()
    c.close()
    conn.close()

def insert_entity(name, desc, site, cameraid):
    #dbpath= r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("""INSERT INTO home_entity(name, desc, site, camera) values(?, ?,?,?)""",(name,desc,site, cameraid))
    conn.commit()
    c.close()
    conn.close()

def insert_imagedata(facenum, imgfullpath, entityid):
    #dbpath= r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO home_imagedata(face_num, created, modified, image, entity) values(?, ?,?,?,?)""",
              (facenum, dat, dat, imgfullpath, entityid)) 
    conn.commit()
    c.close()
    conn.close()

def insert_person(firstname, lastname, birth_date, imgfullpath):
    #dbpath= r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("""INSERT INTO home_person(firstname, lastname, birth_date, face_image) values(?, ?,?,?)""",
              (firstname, lastname, birth_date, imgfullpath)) 
    conn.commit()
    c.close()
    conn.close()

def insert_visiorecognition(fullpathdb, person_id, entity_id, age, gender, emotion):
    dbpath= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
    #dat= datetime.now()
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    sql = "INSERT INTO home_visiorecognition(person, entity, age, gender, emotion) values(?,?,?,?,?)"   
    c.execute(sql,(person_id, entity_id, age, gender, emotion))
    conn.commit()
    c.close()
    conn.close()

def get_persons(fullpathdb, datframe):
    dbpath= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    sql = "SELECT id, firstname,lastname,imagepath,imagename FROM home_person"   
    c.execute(sql)
    datframe=pd.DataFrame(c.fetchall(), columns=['id','firstname','lastname','imagepath','imagename']) 
    print(len(datframe.index))
    #conn.commit()
    c.close()
    conn.close()
    return datframe #consente di vedere nel caller le modifiche a datframe interne al def

def select(fullpathdb, verbose=True):
    dbpath= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    sql = "SELECT * FROM home_camera"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row) 

create_camera()
create_entity()
create_imagedata()
create_person()
create_visiorecognition(dbpath)

conn.close()
