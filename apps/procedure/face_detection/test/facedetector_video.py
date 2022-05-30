# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:37:19 2021

@author: Sergio
"""
import cv2
from mtcnn_cv2 import MTCNN
import time
detector = MTCNN()
thresold=0.8
cap = cv2.VideoCapture(0)

while True: 
    #Capture frame-by-frame
    time.sleep(0.05) #0.02
    __, frame = cap.read()
   
    
    #Use MTCNN to detect faces
    result = detector.detect_faces(frame)
    print(len(result))
    if result != []:
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