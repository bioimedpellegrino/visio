#testextract.py

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 17:16:38 2021

@author: Sergio
"""
import sys
print(sys.version)

import numpy as np
import face_recognition
from tensorflow.keras.models import load_model
import cv2
import time as time
import tensorflow as tf

#imposta db path
#import os.path
#BASE_DIR=os.path.dirname(os.path.abspath(__file__))
#dbfullpath=os.path.join(BASE_DIR,"../../data/visio.sqlite3")
class FaceEmotion:
    def __init__(self):
        sys.path.insert(1, '/home/pi/visiog/procedure')
        import usersel
        self.usel = usersel.Usersel()
        self.dbman= self.usel.dbman
        #GLOBAL VAR per current entityid
        self.entityid= self.dbman.cur_entityid
        self.age = 0
        self.gender= 'female'
        #self.lastname='anonimous-emo'
        self.firstname = self.dbman.emotion_user #'anonymous_emo'
        self.emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 
                            'Surprise': 6, 'Fear': 2, 'Happy': 3}
        self.model = load_model(self.dbman.emotion_modelpath)

    def faceextract(self, image):
        face_locations = face_recognition.face_locations(image)
        print(len(face_locations))
        print(face_locations)
        
        if(len(face_locations)>0):       
            top, right, bottom, left = face_locations[0]
            face_image1 = image[top:bottom, left:right]
            return face_image1,1
        else:
            return image,0

    def faceemotion(self):    
        personcounter = 0
                
        cap = cv2.VideoCapture(0)
        while True:
             time.sleep(0.04) #25 fps
             __, frame = cap.read()
            
             imagetoprocess=np.array(frame)
             resultimage,n= self.faceextract(imagetoprocess)
            
             if(n>0):
                 face_image = cv2.resize(resultimage, (48,48))
                 face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                 face_image = np.reshape(face_image, [1, face_image.shape[0], 
                                                      face_image.shape[1], 1])
                 
                 fimage = tf.cast(face_image, tf.float32)
                 predicted_class = np.argmax(self.model.predict(fimage)) #model.predict(face_image)
                 label_map = dict((v,k) for k,v in self.emotion_dict.items()) 
                 predicted_label = label_map[predicted_class]  
                 print(predicted_label)
                 emotion= predicted_label
                 # aggiungo un anonimous per ogni emotion personid anonimo 
                 lastname = self.firstname + str(personcounter)             
                 self.dbman.insert_person_emotion(self.firstname, lastname, 
                                      self.entityid, self.age, self.gender, emotion)
                 personcounter += 1
             else:
                 predicted_label="no face"
             
              
             cv2.putText(frame,predicted_label,(0,30),cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,0), 1)
             cv2.imshow('frame',frame)
             if cv2.waitKey(1) &0xFF == ord('q'):
                break
        #When everything's done, release capture
        cap.release()
        cv2.destroyAllWindows()
        
    def faceemotion2(self, frame, personcounter):
        imagetoprocess=np.array(frame)
        resultimage,n= self.faceextract(imagetoprocess)
        
        if(n>0): #ADD NUM PERSONE!!!
             face_image = cv2.resize(resultimage, (48,48))
             face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
             face_image = np.reshape(face_image, [1, face_image.shape[0], 
                                                  face_image.shape[1], 1])
             
             fimage = tf.cast(face_image, tf.float32)
             predicted_class = np.argmax(self.model.predict(fimage)) #model.predict(face_image)
             label_map = dict((v,k) for k,v in self.emotion_dict.items()) 
             predicted_label = label_map[predicted_class]  
             print(predicted_label)
             emotion= predicted_label
             # aggiungo un anonimous per ogni emotion personid anonimo 
             lastname = self.firstname + str(personcounter)             
             self.dbman.insert_person_emotion(self.firstname, lastname, 
                                  self.entityid, self.age, self.gender, emotion)
             personcounter += 1
        else:
             predicted_label="no face"
          
        cv2.putText(frame,predicted_label,(0,30),cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,0), 1)
        cv2.imshow('frame',frame)
        
        return personcounter
        #if cv2.waitKey(1) &0xFF == ord('q'):
        #    break
        
    
faceEmotion= FaceEmotion()
faceEmotion.faceemotion()