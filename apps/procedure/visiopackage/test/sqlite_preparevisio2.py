# sqlite_preparevisio2.py
#create folder /home/pi/lab/visio
#mkdir /home/pi/visio

#Give permission for user to folders visio/
#sudo chown -R pi visio/
 
import sqlite3
from datetime import datetime

# create DB /home/pi/visio/data/visiodb.sqlite3
dbpath= r'/home/pi/visio/data/visio.sqlite3'
conn = sqlite3.connect(dbpath)
print(type(conn))
print('db connected')

#t_camera(id, name, desc, timestamp);
#es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)
def create_camera():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_camera (id INTEGER PRIMARY KEY, name TEXT, desc TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")
    except:
        pass

#t_entity(id, name, desc, localita, camera_id, FOREIGN KEY(camera_id));
#può essere un'entrata, un corridoio o un oggetto/evento esposto
def create_entity():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_entity (id INTEGER PRIMARY KEY, name TEXT, desc TEXT, site TEXT, camera_id INTEGER, 
        FOREIGN KEY(camera_id) REFERENCES t_camera(id));""")
    except:
        pass

#t_imagedata(id, face_num,  timestamp, entity_id, FOREIGN KEY(entity_id));
#storage di face detection, ad ogni immagine di un'entita associo il numero di facce rilevate
def create_imagedata():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_imagedata (id INTEGER PRIMARY KEY, face_num INTEGER,  imgfullpath TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
entity_id INTEGER, FOREIGN KEY(entity_id) REFERENCES t_entity(id));""")
    except:
        pass

#t_person(id, firstname,  lastname, gender, birth_date, document_num, imagepath, imagename);
# possono essere persone note con ritratti da confrontare per face recognition oppure 
#nel caso di interesse per sola analisi di (emotion, age, gender) senza face recognition e in riferimento ad un'entity
# "unknown"+counter come firstname
def create_person():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_person (id INTEGER PRIMARY KEY, firstname TEXT,  lastname TEXT, gender TEXT, birth_date DATETIME, 
        min_age REAL,  max_age REAL, document_num TEXT, imagepath TEXT, imagename TEXT);""")
    except:
        pass

#possibile classificazione emotions: happy, sad, fear, anger, surprise, neutral, disgust
#t_person_entity(person_id, entity_id, emotion, emotionval, timestamp);
# possono essere persone riconosciute per quella entita in un dato momento (=timestamp di t_imagedata)
def create_person_entity():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_person_entity (person_id INTEGER, FOREIGN KEY(person_id) REFERENCES t_person(id), entity_id INTEGER, 
        FOREIGN KEY(entity_id) REFERENCES t_entity(id), emotion TEXT, emotionval REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")
    except:
        pass

# es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)     
def insert_picamera(namein, cameradesc):
    dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO t_camera (name, desc, timestamp) values(?, ?,?)""",(namein,cameradesc,dat)) 

def insert_entity(name, desc, site, cameraid):
    c.execute("""INSERT INTO t_entity(name, desc, site, camera_id) values(?, ?,?,?)""",(name,desc,site, cameraid)) 

def insert_imagedata(facenum, imgfullpath, entityid):
    dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO t_imagedata(face_num, imgfullpath, timestamp, entity_id) values(?, ?,?,?)""",(facenum, imgfullpath, dat, entityid)) 

def select(verbose=True):
    sql = "SELECT * FROM t_camera"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row) 

c = conn.cursor()
create_camera()
create_entity()
create_imagedata()
create_person()
create_person_entity()
#create_knownface()

cameraname='camera1'
cameradesc= 'pi camera v.2'
insert_picamera(cameraname, cameradesc)

entname='entry1'
desc='porta1'
site='building1'
camera_id=1
insert_entity(entname, desc, site,camera_id)

conn.commit() #commit needed
select()
c.close()
