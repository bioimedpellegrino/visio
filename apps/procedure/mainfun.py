#mainfun.py

from this import s

import cv2
#from mtcnn_cv2 import MTCNN #test
import sys
print(sys.version)
import time
import tkinter as tk
from tkinter import messagebox


class Main():

    def __init__(self, userselection): #dizionario GUI
         #TEST
        userselection['detection'] = 0
        userselection['recognition'] = 0
        userselection['emotion_agegender'] = 3 #1: solo agegender, 2: solo emotion, 3: emo + agegender
        userselection['show_frame'] = 1
        #end TEST
        self.dict_usel = userselection
        
        sys.path.insert(1, '/home/pi/visio/apps/procedure')
        import usersel    
        self.dbmgr_path = r'/home/pi/visio/apps/procedure/visiopackage'     
        self.usel = usersel.Usersel(self.dbmgr_path)
        
        sys.path.insert(1, '/home/pi/visio/apps/procedure/face_detection')
        import dja_fdetect
        self.facedetection = dja_fdetect.Detection(self.usel)
        
        sys.path.insert(1, '/home/pi/visio/apps/procedure/face_recognition')
        import facerec_faster_sql2
        self.facerecognition = facerec_faster_sql2.FaceRecognition(self.usel)
        
        sys.path.insert(1, '/home/pi/visio/apps/procedure/face_emotion')
        import testextract
        self.faceemotion = testextract.FaceEmotion(self.usel)
        
        sys.path.insert(1, '/home/pi/visio/apps/procedure/face_agegender')
        import face_agegender
        self.agegender=face_agegender.AgeGender(self.usel)
        
    def mainfun(self):
        '''root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('Test', 'mainfun() INIT')
        root.update()'''
        
        #SET PARAMS in SQLITE3 nodjango
        #self.usel.setparams_2Db()
        #self.usel.getparams_fromDb() #get user selections saved in DB
        #self.usel.showparams()
        imgfullpath = self.usel.dbman.imgpath
        imgcounter=0
        personcounter = 0 #Emotion        

        show_frame = self.dict_usel['show_frame'] 
        cap = cv2.VideoCapture(0, cv2.CAP_V4L) #VideoCapture(-1, cv2.CAP_V4L2)
        #cap = cv2.VideoCapture(cv2.CAP_V4L2)
        #if cap.isOpened()==False:
        #    cap.open(-1)      

        #detection, recognition, emotion-agegender
        if self.dict_usel['recognition'] == 1:
            known_face_names = []
            known_face_name_ids = []
            known_face_encodings = []
            known_face_names, known_face_name_ids, known_face_encodings = self.facerecognition.prepareLists(
                    known_face_names, known_face_name_ids, known_face_encodings)
            
        if (self.dict_usel['detection'] == 0 and 
            self.dict_usel['recognition'] == 0 and 
            self.dict_usel['emotion_agegender'] == 1): #solo AGEGENDER
            cap.set(3, 480) #set width of the frame
            cap.set(4, 640)
        
        while True:            
            time.sleep(0.10) #0.04==25 fps
            ret, frame = cap.read()
            if ret==False:
                root = tk.Tk()
                root.withdraw()
                messagebox.showwarning('Test', 'IMAGE Error')
                root.update()
                            
            if (self.dict_usel['detection'] == 1 and 
                self.dict_usel['recognition'] == 1 and 
                self.dict_usel['emotion_agegender'] == 1): 
                print('mainfun() ALL')
                imgcounter = self.facerecognition.facerec_fasterproc(frame, imgcounter, 
                                                       known_face_names, 
                                                       known_face_name_ids, 
                                                       known_face_encodings,
                                                       show_frame) #DETECT + RECO
                #personcounter = faceemotion.faceemotion2(frame, personcounter) #EMOTION
                #agegender.video_detector2(frame, agegender.age_net, agegender.gender_net) #AGEGENDER
                
            elif (self.dict_usel['detection'] == 1 and 
                  self.dict_usel['recognition'] == 0 and 
                  self.dict_usel['emotion_agegender'] == 0):#DETECT
                imgcounter = self.facedetection.facedetect2(frame, imgfullpath, imgcounter)
            elif (self.dict_usel['detection'] == 0 and 
                  self.dict_usel['recognition'] == 1 and 
                  self.dict_usel['emotion_agegender'] == 0): #RECOG                
                imgcounter = self.facerecognition.facerec_fasterproc(frame, imgcounter, 
                                                       known_face_names, 
                                                       known_face_name_ids, 
                                                       known_face_encodings,
                                                       show_frame)
                print('faceCounter = ' + str(imgcounter))
            elif (self.dict_usel['detection'] == 1 and 
                  self.dict_usel['recognition'] == 1 and 
                  self.dict_usel['emotion_agegender'] == 0): #DETECT + RECOG                
                imgcounter = self.facerecognition.facerec_fasterproc(frame, imgcounter, 
                                                       known_face_names, 
                                                       known_face_name_ids, 
                                                       known_face_encodings,
                                                       show_frame)                
            elif (self.dict_usel['detection'] == 0 and 
                  self.dict_usel['recognition'] == 0 and 
                  self.dict_usel['emotion_agegender'] == 0): #VIDEO
                '''root = tk.Tk() 
                root.withdraw()                
                messagebox.showwarning('Test', 'mainfun() VIDEO') 
                root.update()'''
            elif (self.dict_usel['detection'] == 0 and 
                  self.dict_usel['recognition'] == 0 and 
                  self.dict_usel['emotion_agegender'] == 1): #solo AGEGENDER
                 #personcounter = self.faceemotion.faceemotion2(frame, personcounter) #EMOTION
                #DETECTION
                #imgcounter = facedetection.facedetect2(frame, imgfullpath, imgcounter)
                #AGEGENDER
                personcounter = self.agegender.video_detector2(frame, self.agegender.age_net, 
                                                               self.agegender.gender_net) #, personcounter)
            elif (self.dict_usel['detection'] == 0 and 
                  self.dict_usel['recognition'] == 0 and 
                  self.dict_usel['emotion_agegender'] == 2): #solo EMOTION
                '''root = tk.Tk()
                root.withdraw()
                messagebox.showwarning('Test', 'mainfun() EMOTION') 
                root.update()'''
                personcounter = self.faceemotion.faceemotion2(frame, personcounter) #EMOTION
            elif (self.dict_usel['detection'] == 0 and 
                  self.dict_usel['recognition'] == 0 and 
                  self.dict_usel['emotion_agegender'] == 3): #EMOTION + AGEGENDER
                personcounter = self.faceemotion.faceemotion2(frame, personcounter) #EMOTION                
                personcounter = self.agegender.video_detector2(frame, self.agegender.age_net, 
                                                               self.agegender.gender_net) #AGEGENDER
                            
            #display resulting frame
            if self.dict_usel['show_frame'] ==1:
                cv2.imshow('frame',frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) &0xFF == ord('q'):
                break     
        
        #When everything's done, release capture
        cap.release()
        cv2.destroyAllWindows()

#import usersel
#userselection=usersel.Usersel() 
userselection = {} #dictionary    
main= Main(userselection)
main.mainfun()        