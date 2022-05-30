#dja_fdetect.py

import cv2
from mtcnn_cv2 import MTCNN
#import time
import sys

class Detection:
    def __init__(self):
        sys.path.insert(1, '/home/pi/visiog/procedure/visiopackage')
        import djangosqlite_db
        self.djangosqlite_db = djangosqlite_db
        self.dbman = self.djangosqlite_db.Dbmgr()
        self.entityid= self.dbman.cur_entityid
        sys.path.insert(1, '/home/pi/visiog/procedure')
        import self.usersel
        #self.detector = MTCNN()

    def facedetect2(self, frame, imgfullpath, imgcounter):
        self.detector = MTCNN()
        #Use MTCNN to detect faces
        result = self.detector.detect_faces(frame)
        
        if result != []:
            imgcounter=imgcounter+1
            if self.usersel.Usersel().saveimage == 1:
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