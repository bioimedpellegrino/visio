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

#create 2 tables, t_camera, t_imagedata
def create_camera():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_camera (camera_id INTEGER PRIMARY KEY AUTOINCREMENT, desc TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")
    except:
        pass
def create_imagedata():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS t_imagedata (id INTEGER PRIMARY KEY AUTOINCREMENT, face_num INTEGER,  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
camera_id INTEGER, FOREIGN KEY(camera_id) REFERENCES t_camera(camera_id));""")
    except:
        pass
      
def insert_picamera(cameraID, cameradesc):
    dat= datetime.now() #CURRENT_TIMESTAMP
    c.execute("""INSERT INTO t_camera (camera_id, desc, timestamp) values(?, ?, ?)""",(cameraID,cameradesc,dat)) 

def select(verbose=True):
    sql = "SELECT * FROM t_camera"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row) 

c = conn.cursor()
create_camera()
create_imagedata()

cameradesc= 'pi camera v.2'
cameraID=1
insert_picamera(cameraID, cameradesc)

conn.commit() #commit needed
select()
c.close()
