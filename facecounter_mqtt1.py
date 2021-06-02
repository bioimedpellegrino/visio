#retrieve total facenum and sends to mqtt local or in internet
import sqlite3
import pandas as pd #pandas per dataframe
import time

#mqtt
topicname="totTopic"
mqtt_server = "localhost" 
#mqtt_server = "aspoto.dyndns.org"

#mqtt client publish
from paho.mqtt.client import Client
client = Client("Publisher_test")

def on_publish(client, userdata, mid):
 print("Messaggio pubblicato")

client.on_publish = on_publish
client.connect(mqtt_server) 
client.loop_start()

#db sqlite
db_path = r'/home/pi/lab/visio/visiodb.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cameraId = 1
total_face_num=0
counter=0
# ciclo per inviare TOTAL imageNum a mqtt 
while True:
    sql= "SELECT SUM(face_num) FROM t_imagedata WHERE camera_id=?" 
    rec = cursor.execute(sql,(cameraId,))
    reco = cursor.fetchall()
    rec_exists = cursor.fetchall() is not None
    if rec_exists: 
        print(type(reco))
        counter= reco[0][0]
        print(counter)
        if counter != total_face_num:  #publish mqtt
            total_face_num = counter
            client.publish(topic = topicname, payload = total_face_num) #payload = messaggio

    time.sleep(1)

client.loop_stop()
client.disconnect() 
