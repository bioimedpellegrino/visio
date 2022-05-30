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

def create():
    try:
        c.execute("""CREATE TABLE mytable
                 (start, end, score)""")
    except:
        pass

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
db_path = r'/home/pi/lab/sqlitedb/visio.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
create()
insert()
conn.commit() #commit needed
select()
c.close()

#gestione con pandas dataframe
import pandas as pd
conn = sqlite3.connect(db_path)
c = conn.cursor()
sql= "SELECT COUNT(*) FROM mytable"
rec = c.execute(sql)
print(type(rec))
counter= rec[0].value
print(counter)


