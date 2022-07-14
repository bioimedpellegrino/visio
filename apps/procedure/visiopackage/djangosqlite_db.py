# djangosqlite_db.py

#create folder /home/pi/lab/visio
#mkdir /home/pi/visio

#NB: posizione foreign key in create table deve essere sempre dopo ultima colonna!!!

#Give permission for user to folders visio/
#sudo chown -R pi visio/

import pandas as pd 
import sqlite3
from datetime import datetime

class Dbmgr:
    def __init__(self):
        self.dbpath= r'/home/pi/visio/apps/procedure/data/db.sqlite3' # create DB
        self.imgpath= r'/home/pi/visio/apps/pictures/'
        self.portraitpath= self.imgpath + r'portraits/'        
        self.procedurepath= r'/home/pi/visio/apps/procedure/visiopackage'
        self.soundpath= r'/home/pi/visio/apps/procedure/sound/'
        self.emotion_user= 'anonymous_emo'
        self.emotion_modelpath= r'/home/pi/visio/apps/procedure/face_emotion/model_v6_23.hdf5'
        self.cur_entityid=1 #da impostare con entityid valida correntemente
        self.agegen_user= 'anonymous_agegen'
        self.agegender_modelpath= r'/home/pi/visio/apps/procedure/face_agegender/agegender_model/'
        
        self.conn = sqlite3.connect(self.dbpath)
    #print(type(conn))
    #print('conn connected')
    
    def createDB(self):
        self.create_camera()
        self.create_entity()
        self.create_imagedata()
        self.create_person()
        self.create_visiorecognition()
        self.create_param()
        self.conn.close()
    
#CREATE
    def create_param(self): #function > def create_camera(): method > def create_camera(self):
        c = self.conn.cursor() #faceagegender INTEGER,
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS home_param (id INTEGER PRIMARY KEY,
                                                                detection INTEGER,
                                                                recognition INTEGER,
                                                                emotion_agegender INTEGER,
                                                                saveimage INTEGER,
                                                                useaudio INTEGER,
                                                                framelapse REAL);""")
        except:
            pass
        c.close()
        
    #t_camera(id, name, desc, timestamp);
    #es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)
    def create_camera(self): #function > def create_camera(): method > def create_camera(self):
        c = self.conn.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS home_camera (id INTEGER PRIMARY KEY, 
                                                                 name TEXT, 
                                                                 desc TEXT, 
                                                                 user_selection TEXT);""")
        except:
            pass
        c.close()
    
    #t_entity(id, name, desc, localita, camera_id, FOREIGN KEY(camera_id));
    #può essere un'entrata, un corridoio o un oggetto/evento esposto
    def create_entity(self):
        c = self.conn.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS home_entity (id INTEGER PRIMARY KEY, 
                                                                 name TEXT, 
                                                                 desc TEXT, 
                                                                 site TEXT, 
                                                                 camera INTEGER, 
                                                                 FOREIGN KEY(camera) REFERENCES home_camera(id));""")
        except:
            pass
        c.close()
    
    #t_imagedata(id, face_num,  timestamp, entity_id, FOREIGN KEY(entity_id));
    #storage di face detection, ad ogni immagine di un'entita associo il numero di facce rilevate
    def create_imagedata(self):
        c = self.conn.cursor()
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
    def create_person(self):
        c = self.conn.cursor()
        try: #document_num TEXT,
            c.execute("""CREATE TABLE IF NOT EXISTS home_person (id INTEGER PRIMARY KEY, 
                                                                 firstname TEXT,  
                                                                 lastname TEXT, 
                                                                 birth_date DATETIME,  
                                                                 face_image TEXT);""") #imagefullpath
        except Exception as e:
            print(e)
            pass
        c.close()
    
    #possibile classificazione emotions: happy, sad, fear, anger, surprise, neutral, disgust
    #t_person_entity(person_id, entity_id, emotion, emotionval, timestamp);
    # possono essere persone riconosciute per quella entita in un dato momento (=timestamp di t_imagedata)
    #Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3
    
    def create_visiorecognition(self): #(self,fullpathdb)
        #dbpath1= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
        conn1 = sqlite3.connect(self.dbpath)
        print('db connected pers_ent')
        cu = conn1.cursor()
        try:
            cu.execute("""CREATE TABLE IF NOT EXISTS home_visiorecognition(id INTEGER PRIMARY KEY, 
                                    person INTEGER not null, entity INTEGER not null,
                                    age REAL, 
                                    gender TEXT,
                                    emotion TEXT,
                                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    foreign key(person) references home_person(id) on delete cascade,
                                    FOREIGN KEY(entity) REFERENCES home_entity(id) on delete cascade);""")
        except Exception as e:
            print(e)
            pass
        conn1.commit()
        cu.close()
        conn1.close()
#INSERT        
    def insert_param(self, facedetection, facerecognition, emotion_agegender, saveimage, useaudio, framelapse):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        c.execute("""INSERT INTO home_param (detection, recognition,
                                             emotion_agegender, 
                                             saveimage, useaudio, framelapse) values(?,?,?,?,?,?)""",
                (facedetection, facerecognition, emotion_agegender, saveimage, useaudio, framelapse))
        self.conn.commit()
        c.close()
        self.conn.close()
        
    # es. (id=1, name=picamera1, desc=camera8MP, 2021-08-10)     
    def insert_picamera(self, namein, cameradesc, usersel):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        #dat= datetime.now() #CURRENT_TIMESTAMP
        c.execute("""INSERT INTO home_camera (name, desc, user_selection) values(?,?,?)""",(namein,cameradesc, usersel))
        self.conn.commit()
        c.close()
        self.conn.close()
    
    def insert_entity(self, name, desc, site, cameraid):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        c.execute("""INSERT INTO home_entity(name, desc, site, camera) values(?, ?,?,?)""",(name,desc,site, cameraid))
        self.conn.commit()
        c.close()
        self.conn.close()
    
    def insert_imagedata(self, facenum, imgfullpath, entityid):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        dat= datetime.now() #CURRENT_TIMESTAMP
        c.execute("""INSERT INTO home_imagedata(face_num, created, modified, image, entity) values(?, ?,?,?,?)""",
                  (facenum, dat, dat, imgfullpath, entityid)) 
        self.conn.commit()
        c.close()
        self.conn.close()
    
    def insert_person(self, firstname, lastname, birth_date, imgfullpath):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        c.execute("""INSERT INTO home_person(firstname, lastname, birth_date, face_image) values(?, ?,?,?)""",
                  (firstname, lastname, birth_date, imgfullpath)) 
        self.conn.commit()
        personid = c.lastrowid
        c.close()
        self.conn.close()
        return personid
    #inserisce una new person and his emotion
    def insert_person_emotion(self, firstname, lastname, entityid, age, gender, emotion):
        #insert person
        birth_date=''
        imgfullpath=''
        personid = self.insert_person(firstname, lastname, birth_date, imgfullpath)
        #age=0
        #gender='female'
        self.insert_visiorecognition(personid, entityid, age, gender, emotion)
            
    def insert_visiorecognition(self, person_id, entity_id, age, gender, emotion):
        #dat= datetime.now()
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = "INSERT INTO home_visiorecognition(person, entity, age, gender, emotion,date) values(?,?,?,?,?,?)"   
        c.execute(sql,(person_id, entity_id, age, gender, emotion, datetime.now()))
        self.conn.commit()
        c.close()
        self.conn.close()
#GETS    
    def get_persons(self, datframe): #self, fullpathdb, datframe
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = "SELECT id, firstname,lastname,face_image FROM home_person"   
        c.execute(sql)
        datframe=pd.DataFrame(c.fetchall(), columns=['id','firstname','lastname','face_image']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe #consente di vedere nel caller le modifiche a datframe interne al def

    def get_persons_img(self, datframe): #self, fullpathdb, datframe
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = 'SELECT id, firstname,lastname,face_image FROM home_person WHERE face_image != ""'   
        c.execute(sql)
        datframe=pd.DataFrame(c.fetchall(), columns=['id','firstname','lastname','face_image']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe #consente di vedere nel caller le modifiche a datframe interne al def
    
    def get_person(self, lastname, datframe):
        #self.conn = sqlite3.connect(dbpath1)
        c = self.conn.cursor()
        sql = "SELECT id, firstname,lastname FROM home_person WHERE lastname = " + lastname  
        c.execute(sql)
        datframe=pd.DataFrame(c.fetchall(), columns=['id','firstname','lastname']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe #consente di vedere nel caller le modifiche a datframe interne al def
    
    def get_visiorecognitions(self, datframe):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = "SELECT id, person, entity, age, gender, emotion, date FROM home_visiorecognition"  
        c.execute(sql)
        datframe=pd.DataFrame(c.fetchall(), 
                        columns=['id','person','entity', 'age', 'gender', 'emotion', 'date']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe 
    
    def get_entities(self, datframe):
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = "SELECT id, name, desc, site, camera FROM home_entity"  
        c.execute(sql)
        datframe=pd.DataFrame(c.fetchall(), 
                        columns=['id','name','desc', 'site', 'camera']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe 
    
#PARAMS
    def get_params(self, datframe, id):
        #self.conn = sqlite3.connect(dbpath1)
        self.conn = sqlite3.connect(self.dbpath)
        c = self.conn.cursor()
        sql = "SELECT * FROM home_param WHERE id = ?"  
        c.execute(sql, str(id))
        datframe=pd.DataFrame(c.fetchall(), columns=['id', 'detection', 'recognition', 
                              'emotion_agegender', 'saveimage', 'useaudio', 'framelapse']) 
        print(len(datframe.index))
        #conn.commit()
        c.close()
        self.conn.close()
        return datframe #consente di vedere nel caller le modifiche a datframe interne al def

#UPDATE
    def update_params(self, id, facedetection, facerecognition, facemotion_agegender, saveimage, 
                      useaudio, framelapse):
        try:
            self.conn = sqlite3.connect(self.dbpath)
            c = self.conn.cursor()
            sql = """UPDATE home_param SET detection = ?, recognition = ?, emotion_agegender = ?, 
            saveimage = ?, useaudio = ?, framelapse = ? WHERE id = ?"""
            data = (facedetection, facerecognition, facemotion_agegender, saveimage, 
                    useaudio, framelapse, id)
            c.execute(sql, data)
            self.conn.commit()
            c.close()            
        except sqlite3.Error as error:
            print("Failed to update sqlite home_param", error)
        finally:
            self.conn.close()
    
    def select(self, fullpathdb, verbose=True):
        dbpath1= fullpathdb #r'/home/pi/visio/data/visio.sqlite3'
        self.conn = sqlite3.connect(dbpath1)
        c = self.conn.cursor()
        sql = "SELECT * FROM home_camera"
        recs = c.execute(sql)
        if verbose:
            for row in recs:
                print(row)
#DELETE                
    def deleteVisioRec(self, entity):
        try:
            self.conn = sqlite3.connect(self.dbpath)
            c = self.conn.cursor()
            sql = """DELETE FROM home_visiorecognition WHERE entity = ?"""
            data = int(entity)
            c.execute(sql, (data,))
            self.conn.commit()
            c.close()            
        except sqlite3.Error as error:
            print("Failed to delete sqlite home_visirecognition", error)
        finally:
            self.conn.close()
#POPULATE            
    def populateDB(self):
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

dbman= Dbmgr()
dbman.create_camera()
dbman.create_entity()
dbman.create_imagedata()
dbman.create_person()
dbman.create_visiorecognition()
dbman.create_param()

dbman.conn.close()
