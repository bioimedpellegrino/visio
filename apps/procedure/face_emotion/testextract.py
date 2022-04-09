# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 17:16:38 2021

@author: Sergio
"""
import sys
print(sys.version)
#query db
sys.path.insert(1,'/home/pi/visio/visiopackage/sqlite')
import sqlitevisio_db

#imposta db path
import os.path
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
dbfullpath=os.path.join(BASE_DIR,"../../data/visio.sqlite3")

#GLOBAL VAR per current entityid ???
entityid=1

import numpy as np
import face_recognition
from tensorflow.keras.models import load_model
import cv2
import time as time
import tensorflow as tf

emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
model = load_model("/home/pi/visio/procs/face_emotion/model_v6_23.hdf5")

def faceextract(image):
    face_locations = face_recognition.face_locations(image)
    print(len(face_locations))
    print(face_locations)
    
    if(len(face_locations)>0):       
        top, right, bottom, left = face_locations[0]
        face_image1 = image[top:bottom, left:right]
        return face_image1,1
    else:
        return image,0


cap = cv2.VideoCapture(0)
while True:
     time.sleep(0.04) #25 fps
     __, frame = cap.read()
    
     imagetoprocess=np.array(frame)
     resultimage,n=faceextract(imagetoprocess)
    
     if(n>0):
         face_image = cv2.resize(resultimage, (48,48))
         face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
         face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])
         
         fimage = tf.cast(face_image, tf.float32)
         predicted_class = np.argmax(model.predict(fimage)) #model.predict(face_image)
         label_map = dict((v,k) for k,v in emotion_dict.items()) 
         predicted_label = label_map[predicted_class]  
         print(predicted_label)
         # add personid anonimo ???
         sqlitevisio_db.add_person_entity_emo(dbfullpath, personid, entityid, predicted_label)
     else:
         predicted_label="no face"
     
      
     cv2.putText(frame,predicted_label,(0,30),cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,0), 1)
     cv2.imshow('frame',frame)
     if cv2.waitKey(1) &0xFF == ord('q'):
        break
#When everything's done, release capture
cap.release()
cv2.destroyAllWindows()