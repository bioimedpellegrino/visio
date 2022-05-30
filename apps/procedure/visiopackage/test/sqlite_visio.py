#create table

import sqlite3


#create DB ?
con = sqlite3.connect'words.db'
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE vocab(vocab_id INTEGER PRIMARY KEY, word TEXT)")
#cur.execute("CREATE TABLE definitions (def_id INTEGER, def TEXT,"
#           "word_def INTEGER, FOREIGN KEY(word_def) REFERENCES vocab(vocab_id))")
#CREATE TABLE IF NOT EXISTS t_camera (camera_id INTEGER PRIMARY KEY AUTOINCREMENT, desc TEXT);
#CREATE TABLE IF NOT EXISTS t_imagedata (id INTEGER PRIMARY KEY AUTOINCREMENT, face_num INTEGER,  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
#camera_id INTEGER, FOREIGN KEY(camera_id) REFERENCES t_camera(camera_id));

def create1():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_camera (camera_id INTEGER PRIMARY KEY AUTOINCREMENT, desc TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")
    except:
        pass
def create2():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_imagedata (id INTEGER PRIMARY KEY AUTOINCREMENT, face_num INTEGER,  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
camera_id INTEGER, FOREIGN KEY(camera_id) REFERENCES t_camera(camera_id));""")
    except:
        pass
      
def insertpi():
    cameraID=1
    c.execute("""INSERT INTO t_camera (camera_id, desc, timestamp)
              values(1, picamera)""")      
      
def insert():
    c.execute("""INSERT INTO mytable (start, end, score)
              values(1, 99, 123)""")

def select(verbose=True):
    sql = "SELECT * FROM mytable"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print row

#db_path = r'C:\Users\Prosserc\Documents\Geocoding\test.db'
db_path = r'/home/pi/lab/visio/visiodb.sqlite3'
conn = sqlite3.connect(db_path)
c = conn.cursor()
create1()
create2()
insertpi()
conn.commit() #commit needed
#select()
c.close()

import sqlite3
import pandas as pd

db_path = r'/home/pi/lab/visio/visiodb.sqlite3'
# ciclo per inviare TOTAL imageNum a mqtt 
#pandas per dataframe
imagenum=0

conn = sqlite3.connect(db_path)
c = conn.cursor()
while true:
  sql= "SELECT COUNT(*) FROM t_imagedata"
  rec = c.execute(sql)
  print(type(rec))
  counter= rec[0].value
  print(counter)
  if counter<> imagenum:
    imagenum = counter
    #publish mqtt
  sleep(1000);  
