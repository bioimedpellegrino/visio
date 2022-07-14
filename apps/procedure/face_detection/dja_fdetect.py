#dja_fdetect.py

import cv2
from mtcnn_cv2 import MTCNN
#import time
#import sys
from usersel import Usersel

class Detection:
    def __init__(self, userse: Usersel):  
        self.dbman = userse.dbman
        self.entityid= self.dbman.cur_entityid
        self.usersel = userse
        #self.detector = MTCNN()

    def facedetect2(self, frame, imgfullpath, imgcounter):
        self.detector = MTCNN()
        #Use MTCNN to detect faces
        result = self.detector.detect_faces(frame)
        
        if result != []:
            imgcounter=imgcounter+1
            if self.usersel.saveimage == 1:
                cv2.imwrite(imgfullpath+str(imgcounter)+'.jpg', frame)      
                self.dbman.insert_imagedata(len(result), str(imgcounter)+'.jpg', self.entityid)
            else:
                self.dbman.insert_imagedata(len(result), '', self.entityid)
                
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
                
        return imgcounter