#1 recupera image da video
#2 face detection
#3 spedisce detected_facenum a topic (=fTopic) di mqtt 
#4 if detected_facenum > 0
#       add record(detected_facenum, timestamp) to table 
#       t_imagedata (db= /home/pi/lab/visio/visiodb.sqlite3, t_camera.id = 1)

#salvare in sqlite table img info num faces + timestamp
import sqlite3
from datetime import datetime

#parametri sqlite db
cameraId = 1
dbpath= r'/home/pi/lab/visio/visiodb.sqlite3'
conn = sqlite3.connect(dbpath)
c = conn.cursor()
def insert_facenum(id, facenum, cameraId):
    dat= datetime.now()
    c.execute('''INSERT INTO t_imagedata values(?,?,?,?)'''(id, facenum, dat, cameraId))
    
def insert_facenum2(facenum, cameraId): #poiche id autoincrement, non imposto
    dat=datetime.now()
    cursor = conn.cursor() 
    cursor.execute('''INSERT INTO t_imagedata(face_num, timestamp, camera_Id) values(?, ?,?)''',(facenum,dat,cameraId))
    cursor.close()    

#parametri mqtt
mqtt_broker= "localhost" #broker ‘localhost’
#mqtt_broker= "aspoto.dyndns.org"
topic_name = "fTopic"

#mqtt publish
from paho.mqtt.client import Client
client = Client("Publisher_test")
def on_publish(client, userdata, mid):
 print("Messaggio pubblicato")
client.on_publish = on_publish
client.connect(mqtt_broker) 

client.loop_start()
#messaggio = input("Inserisci il testo da inviare al topic test")
#face_num =4 #from mtcnn
#client.publish(topic = "fTopic", payload = face_num) #payload = messaggio
#client.loop_stop()
#client.disconnect() 

#mtcnn on video
import cv2
from mtcnn_cv2 import MTCNN
import time

#parametri mtcnn
threshold=0.87

detector = MTCNN()
#print(type(detector))

#test
#imshow funziona su debian con UI!
#test_pic = "test1.jpg"
#test_ris="face_detected.jpg"

#image=cv2.imgread(test_pic)
#image = cv2.cvtColor(cv2.imread(test_pic), cv2.COLOR_BGR2RGB)
cap=cv2.VideoCapture(0)
while True:
    #capture frame by frame
    time.sleep(0.02)
    __, frame=cap.read()
    
    i=0
    result = detector.detect_faces(frame)
    print(len(result))
    if result != []:
            for person in result:
                print(person['confidence'])
                if(person['confidence']>threshold):
                    i=i+1
                    bounding_box=person['box']
                    keypoints=person['keypoints']
                    cv2.rectangle(frame,
                              (bounding_box[0], bounding_box[1]),
                              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                              (0,155,255),
                              2)

                    cv2.circle(frame,(keypoints['left_eye']), 2, (0,155,255), 2)
                    cv2.circle(frame,(keypoints['right_eye']), 2, (0,155,255), 2)
                    cv2.circle(frame,(keypoints['nose']), 2, (0,155,255), 2)
                    cv2.circle(frame,(keypoints['mouth_left']), 2, (0,155,255), 2)
                    cv2.circle(frame,(keypoints['mouth_right']), 2, (0,155,255), 2)
            
            #if i>0:
            face_num =i 
            client.publish(topic = topic_name, payload = face_num)
            #sqlite
            if i>0:
              print(face_num)
              insert_facenum2(face_num, cameraId)
              conn.commit()
    #display resulting frame
    #cv2.imshow('frame', frame) #corretto in debian con UI
    if cv2.waitKey(1) & 0xFF == ord('q'): #stop digitando 1
        break
        
#when everything done, release
cap.release()
cv2.destroyAllWindows()
#mqtt stop
client.loop_stop()
client.disconnect()
#sqlite cursor close
c.close()
