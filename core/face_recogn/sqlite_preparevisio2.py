# sqlite_preparevisio2.py
#create folder /home/pi/lab/visio
mkdir /home/pi/lab/visio

#Give permission for user to folders visio/
sudo chown -R pi visio/

 
import sqlite3
from datetime import datetime

# create DB /home/pi/lab/visio/visiodb.sqlite3
dbpath= r'/home/pi/lab/visio/visiodb.sqlite3'
conn = sqlite3.connect(dbpath)
print(type(conn))
print('db connected')

#t_camera(id, name, desc, timestamp);
#es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)
def create_camera():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_camera (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, desc TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")
    except:
        pass

#t_entity(id, name, desc, localita, camera_id, FOREIGN KEY(camera_id));
#può essere un'entrata, un corridoio o un oggetto/evento esposto
def create_entity():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_entity (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, desc TEXT, localita TEXT, camera_id INTEGER, 
        FOREIGN KEY(camera_id) REFERENCES t_camera(id));""")
    except:
        pass

#t_imagedata(id, face_num,  timestamp, entity_id, FOREIGN KEY(entity_id));
#storage di face detection, ad ogni immagine di un'entita associo il numero di facce rilevate
def create_imagedata():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_imagedata (id INTEGER PRIMARY KEY AUTOINCREMENT, face_num INTEGER,  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
entity_id INTEGER, FOREIGN KEY(entity_id) REFERENCES t_entity(id));""")
    except:
        pass

#t_person(id, firstname,  lastname, gender, birth_date, document_num, imagepath, imagename);
# possono essere persone note con ritratti da confrontare per face recognition oppure 
#nel caso di interesse per sola analisi di (emotion, age, gender) senza face recognition e in riferimento ad un'entity
# "unknown"+counter come firstname
def create_person():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_person (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT,  lastname TEXT, gender TEXT, birth_date DATETIME, 
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
def insert_picamera(cameraID, name, cameradesc):
    dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO t_camera (id, name, desc, timestamp) values(?, ?, ?)""",(cameraID,name,cameradesc,dat)) 

def select(verbose=True):
    sql = "SELECT * FROM t_camera"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row) 

c = conn.cursor()
create_camera()
create_imagedata()
create_knownface()

cameradesc= 'pi camera v.2'
cameraID=1
insert_picamera(cameraID, cameradesc)

conn.commit() #commit needed
select()
c.close()
