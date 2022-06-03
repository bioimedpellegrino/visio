#mainfun.py

import cv2
import sys
print(sys.version)
import sys
import time

#procpath = '/home/pi/visiog/procedure'
#sys.path.insert(1, procpath)
#import usersel
#sys.path.insert(1, '/home/pi/visiog/procedure/face_detection')
#import dja_fdetect

#sys.path.insert(1, '/home/pi/visiog/procedure/face_recognition')
#import facerec_faster_sql2

#sys.path.insert(1, '/home/pi/visiog/procedure/face_emotion')
#import testextract

#sys.path.insert(1, '/home/pi/visiog/procedure/face_agegender')
#import face_agegender

class Main():
    def __init__(self):
        sys.path.insert(1, '/home/pi/visio/procedure')
        import usersel
        self.usersel = usersel
        sys.path.insert(1, '/home/pi/visio/procedure/face_detection')
        import dja_fdetect
        self.dja_fdetect = dja_fdetect
        sys.path.insert(1, '/home/pi/visio/procedure/face_recognition')
        import facerec_faster_sql2
        self.facerec_faster_sql2 = facerec_faster_sql2
        sys.path.insert(1, '/home/pi/visio/procedure/face_emotion')
        import testextract
        self.testextract = testextract
        sys.path.insert(1, '/home/pi/visio/procedure/face_agegender')
        import face_agegender
        self.face_agegender=face_agegender       
        
    def mainfun(self):
        usel = self.usersel.Usersel()
        usel.getparams_fromDb() #get user selections saved in DB
        usel.showparams()
        imgfullpath = usel.dbman.imgpath
        imgcounter=0
        personcounter = 0 #Emotion
        faceemotion = self.testextract.FaceEmotion()
        agegender = self.face_agegender.AgeGender()
        facerecognition = self.facerec_faster_sql2.FaceRecognition()
        facedetection = self.dja_fdetect.Detection()
        
        cap = cv2.VideoCapture(0, cv2.CAP_V4L) #cap = cv2.VideoCapture(0)
        
        #detection, recognition, emotion-agegender
        if usel.recognition == 1:
            known_face_names = []
            known_face_name_ids = []
            known_face_encodings = []
            known_face_names, known_face_name_ids, known_face_encodings = self.facerec_faster_sql2.prepareLists(
                    known_face_names, known_face_name_ids, known_face_encodings)
        
        while True: 
            #Capture frame-by-frame
            time.sleep(usel.framelapse) #0.04==25 fps
            __, frame = cap.read()
            
            #imgcounter = imgcounter + 1
            if usel.detection == 1 and usel.recognition == 1 and usel.emotion_agegender == 1: 
                print('mainfun() ALL')
                imgcounter = facerecognition.facerec_fasterproc(frame, imgcounter, 
                                                       known_face_names, 
                                                       known_face_name_ids, 
                                                       known_face_encodings) #DETECT + RECO
                personcounter = faceemotion.faceemotion2(frame, personcounter) #EMOTION
                agegender.video_detector2(frame, agegender.age_net, agegender.gender_net) #AGEGENDER
                
            elif usel.detection == 1 and usel.recognition == 0 and usel.emotion_agegender == 0:#DETECT
                imgcounter = facedetection.facedetect2(frame, imgfullpath, imgcounter)
                print('mainfun() detect')
            elif usel.detection == 1 and usel.recognition == 1 and usel.emotion_agegender == 0: #DETECT + RECOG
                print('mainfun() recog + detect')
                imgcounter = facerecognition.facerec_fasterproc(frame, imgcounter, 
                                                       known_face_names, 
                                                       known_face_name_ids, 
                                                       known_face_encodings)
            elif usel.detection == 0 and usel.recognition == 0 and usel.emotion_agegender == 0:
               print('mainfun() VIDEO') 
            elif usel.detection == 1 and usel.recognition == 0 and usel.emotion_agegender == 1:
                print('mainfun() detect + emo + agegender')
                personcounter = faceemotion.faceemotion2(frame, personcounter) #EMOTION
                #DETECTION
                imgcounter = facedetection.facedetect2(frame, imgfullpath, imgcounter)
                #AGEGENDER
                agegender.video_detector2(frame, agegender.age_net, agegender.gender_net) #, personcounter)
            
            #display resulting frame
            #cv2.imshow('frame',frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) &0xFF == ord('q'):
                break     
        
        #When everything's done, release capture
        cap.release()
        cv2.destroyAllWindows()
        
main= Main()
main.mainfun()        