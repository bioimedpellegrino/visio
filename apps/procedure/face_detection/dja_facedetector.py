#https://pypi.org/project/mtcnn-opencv/
# MTCNN-OpenCV
# MTCNN Face Detector using OpenCV, no reqiurement for tensorflow/pytorch.
#sudo su
#apt update
#apt upgrade

#INSTALLATION
#pip3 install opencv-python
#pip3 install opencv-python-headless
#pip3 install mtcnn-opencv
#restart os

# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:37:19 2021

@author: Sergio
"""
import cv2
from mtcnn_cv2 import MTCNN
import time

procedurepath = '/home/pi/visiog/visiopackage/sqlite'
procpath = '/home/pi/visiog/procedure'
procfilename='djangosqlite_db'

import sys
sys.path.insert(1, procedurepath)
import djangosqlite_db

sys.path.insert(1, procpath)
import usersel

#usersel = usersel.Usersel()

#from sqlite_visio2.py import
entityid= djangosqlite_db.Dbmgr().cur_entityid


# SALVA IMMAGINI: converti in parametro
def facedetect(saveimage):
    detector = MTCNN()
    #thresold=0.8
    imgcounter=0
    cap = cv2.VideoCapture(0, cv2.CAP_V4L)
    
    dbman= djangosqlite_db.Dbmgr()
    imgfullpath = dbman.imgpath #'/home/pi/visiog/pictures/'
    
    while True: 
        #Capture frame-by-frame
        time.sleep(0.04) #0.02
        __, frame = cap.read()
        
        #Use MTCNN to detect faces
        result = detector.detect_faces(frame)
        print(len(result))
    #    sqlitevisio_db.insert_imagedata(len(result), imgfullpath, entityid)
        if result != []:
            imgcounter=imgcounter+1
            if saveimage == True:
                cv2.imwrite(imgfullpath+str(imgcounter)+'.jpg', frame)      
                dbman.insert_imagedata(len(result), str(imgcounter)+'.jpg', entityid)
            else:
                dbman.insert_imagedata(len(result), '', entityid)
                
            for person in result:
                bounding_box = person['box']
                keypoints = person['keypoints']
        
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
        #display resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    #When everything's done, release capture
    cap.release()
    cv2.destroyAllWindows()

#param per salvare immagine di facce rilevate
#saveimage=True    
facedetect(usersel.Usersel().saveimage)