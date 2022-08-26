#mainfun.py

from this import s

import cv2
#from mtcnn_cv2 import MTCNN #test
import sys
print(sys.version)
import time
import tkinter as tk
from tkinter import messagebox
#import numpy as np
from datetime import datetime
from collections import defaultdict


class Main():

    def __init__(self, userselection): #dizionario GUI
         #TEST
        userselection['detection'] = 0
        userselection['recognition'] = 0
        userselection['emotion_agegender'] = 0 #1: solo agegender, 2: solo emotion, 3: emo + agegender
        userselection['show_frame'] = 0
        userselection['numfaces_graphic'] = 0
        userselection['emotions_graphic'] = 0
        userselection['gender_graphic'] = 0
        userselection['age_graphic'] = 0
        userselection['recognized_graphic'] = 1
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
        self.usel.detection = userselection['detection']
        self.usel.recognition = userselection['recognition']
        self.usel.emotion_agegender = userselection['emotion_agegender']                
        #SET PARAMS in SQLITE3 nodjango
        self.usel.setparams_2Db()
        #self.usel.getparams_fromDb() #get user selections saved in DB
        self.usel.showparams()
        imgfullpath = self.usel.dbman.imgpath
        imgcounter=0
        personcounter = 0 #Emotion
        personcounter1 = 0

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
            
        if userselection['numfaces_graphic'] == 1:
            init= datetime.strptime('2022-07-23 00:00:00', '%Y-%m-%d %H:%M:%S')
            end= datetime.strptime('2022-07-24 23:59:59', '%Y-%m-%d %H:%M:%S')
            timerange = 15
            entityId = self.usel.dbman.cur_entityid #1
            facenum_dict= self.show_numfaces_graphic(init, end, timerange, entityId)
            print(facenum_dict)
        elif userselection['emotions_graphic'] == 1:
            init= datetime.strptime('2022-07-23 00:00:00', '%Y-%m-%d %H:%M:%S')
            end= datetime.strptime('2022-07-24 23:59:59', '%Y-%m-%d %H:%M:%S')
            timerange = 15
            entityId = self.usel.dbman.cur_entityid
            emotions_dict= self.show_emo_graphic(init, end, timerange, entityId)
            print(emotions_dict)            
        elif userselection['gender_graphic'] == 1:
            init= datetime.strptime('2022-07-23 00:00:00', '%Y-%m-%d %H:%M:%S')
            end= datetime.strptime('2022-07-24 23:59:59', '%Y-%m-%d %H:%M:%S')
            timerange = 15
            entityId = self.usel.dbman.cur_entityid
            gender_dict= self.show_gender_graphic(init, end, timerange, entityId)
            print(gender_dict)
        elif userselection['age_graphic'] == 1:
            init= datetime.strptime('2022-07-23 00:00:00', '%Y-%m-%d %H:%M:%S')
            end= datetime.strptime('2022-07-24 23:59:59', '%Y-%m-%d %H:%M:%S')
            timerange = 15
            entityId = self.usel.dbman.cur_entityid
            age_dict= self.show_age_graphic(init, end, timerange, entityId)
            print(age_dict) 
        elif userselection['recognized_graphic'] == 1:
            init= datetime.strptime('2022-07-23 00:00:00', '%Y-%m-%d %H:%M:%S')
            end= datetime.strptime('2022-07-24 23:59:59', '%Y-%m-%d %H:%M:%S')
            timerange = 15
            entityId = self.usel.dbman.cur_entityid
            recocgnized_dict= self.show_recognized_graphic(init, end, timerange, entityId)
            print(recocgnized_dict)                       
        else:
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
                    personcounter1 = self.faceemotion.faceemotion2(frame, personcounter1) #EMOTION                
                    personcounter = self.agegender.video_detector2(frame, self.agegender.age_net, 
                                                                   self.agegender.gender_net) #AGEGENDER
                elif (self.dict_usel['detection'] == 1 and #detect
                      self.dict_usel['recognition'] == 0 and 
                      self.dict_usel['emotion_agegender'] == 3): #EMOTION + AGEGENDER
                    personcounter1 = self.faceemotion.faceemotion2(frame, personcounter1) #EMOTION                
                    personcounter = self.agegender.video_detector2(frame, self.agegender.age_net, 
                                                                   self.agegender.gender_net) #AGEGENDER
                    imgcounter = self.facedetection.facedetect2(frame, imgfullpath, imgcounter)            
                #display resulting frame
                if self.dict_usel['show_frame'] ==1:
                    cv2.imshow('frame',frame)
                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) &0xFF == ord('q'):
                    break     
        
        #When everything's done, release capture
            cap.release()
            cv2.destroyAllWindows()

    def show_numfaces_graphic(self, init:datetime, end:datetime, timerange, entityId):
        facenum_dict= defaultdict(list)  #dictionary of lists 
        facenum_dict.clear()
        facenum_dict = self.usel.get_facenum_in_period(init, end, timerange, 
                                                       entityId, facenum_dict)
        return facenum_dict 

            
    def show_emo_graphic(self, init:datetime, end:datetime, timerange, entityId):
        '''Angry':0,'Disgust':1,'Fear':2,'Happy':3,'Neutral':4,'Sad':5,'Surprise':6'''
        emotypeDict={0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral',
                     5:'Sad', 6:'Surprise'}
        emotions_dict= defaultdict(list)  #dictionary of lists 
        emotions_dict.clear()
        emotions_dict = self.usel.get_emo_in_period(init, end, timerange, 
                                    entityId, emotypeDict, emotions_dict)
        return emotions_dict 
    
#nello stesso timerange [male, male_num, female, female_num] se almeno uno > 0
    def show_gender_graphic(self, init:datetime, end:datetime, timerange, entityId):
        gendertypeDict={0:'Male', 1:'Female'}
        
        gender_dict= defaultdict(list)  #dictionary of lists 
        gender_dict.clear()
        gender_dict = self.usel.get_gender_in_period(init, end, timerange, 
                                    entityId, gendertypeDict, gender_dict)
        return gender_dict 

    def show_age_graphic(self, init:datetime, end:datetime, timerange, entityId):
        agetypeDict={0:'(0, 2)', 1:'(4, 6)', 2:'(8, 12)', 3:'(15, 20)',
                     4:'(25, 32)', 5:'(38, 43)', 6:'(48, 53)', 7:'(60, 100)'}
        
        age_dict= defaultdict(list)  #dictionary of lists 
        age_dict.clear()
        age_dict = self.usel.get_age_in_period(init, end, timerange, 
                                    entityId, agetypeDict, age_dict)
        return age_dict    

#num persone riconosciute nel periodo
    def show_recognized_graphic(self, init:datetime, end:datetime, timerange, entityId):
        
        genderval='recog-nogender'
        recognized_dict= defaultdict(list)  #dictionary of lists 
        recognized_dict.clear()
        recognized_dict = self.usel.get_recognized_in_period(init, end, timerange, 
                              entityId, genderval, recognized_dict)
        
        return recognized_dict        
          
#import usersel
#userselection=usersel.Usersel() 
userselection = {} #dictionary    
main= Main(userselection)
main.mainfun()        