#face_agegender.py

import cv2
#import numpy as np
#import pafy
import sys


class AgeGender:
    def __init__(self):
        #sys.path.insert(1,'/home/pi/visiog/procedure/visiopackage')
        #import self.djangosqlite_db
        sys.path.insert(1, '/home/pi/visiog/procedure')
        import usersel
        self.usel = usersel.Usersel()
        self.cap = cv2.VideoCapture(0)
        #cap.set(propId, value), here 3 is the propertyId of width and 4 is for Height.
        self.cap.set(3, 480) #set width of the frame
        self.cap.set(4, 640) #set height of the frame
        #3 separate lists for storing Model_Mean_Values, Age and Gender.
        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self.age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
        self.gender_list = ['Male', 'Female']
        self.modelfullpath= self.usel.dbman.agegender_modelpath #"/home/pi/visio/procs/face_agegender/agegender_model/" 
        self.age_net, self.gender_net = self.load_caffe_models()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.firstname = self.usel.dbman.agegen_user
        self.entityid= self.usel.dbman.cur_entityid
        self.emotion= '-'

    def load_caffe_models(self):
        age_net = cv2.dnn.readNetFromCaffe(self.modelfullpath + 'deploy_age.prototxt', 
                                           self.modelfullpath +'age_net.caffemodel')
        gender_net = cv2.dnn.readNetFromCaffe(self.modelfullpath + 'deploy_gender.prototxt', 
                                              self.modelfullpath + 'gender_net.caffemodel')
    
        return(age_net, gender_net)

    def video_detector(self, age_net, gender_net):
      #font = cv2.FONT_HERSHEY_SIMPLEX
      
      firstname = self.usel.dbman.agegen_user
      entityid= self.usel.dbman.cur_entityid
      personcounter=0
      emotion= ''
    
      while True:
        ret1=False
        ret, image = self.cap.read()
        if (ret==False and self.cap.isOpened()==False):
            ret1 = self.cap.open(play.url) #da passare come param
        if (ret==False and ret1==False):
          print('Error in open video')
      
      #Load the pre-built model for facial detection
        #cascade_path= modelfullpath + 'haarcascade_frontalface_alt.xml' 
        #print(cascade_path)
      #face_cascade = cv2.CascadeClassifier(modelfullpath + 'haarcascade_frontalface_alt.xml')
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                             'haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
     
      #OpenCV face detector expects gray images e quindi conversione in gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    #detect faces from an image. Params: grayscale image, scaleFactor, minNeighbors
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
        if(len(faces)>0):
          print("Found {} faces".format(str(len(faces))))
    
        #Loop through the list of faces and draw rectangles on the human faces
        for (x, y, w, h )in faces:
          cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
          #Get Face 
          face_img = image[y:y+h, h:h+w].copy()
          blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), self.MODEL_MEAN_VALUES, 
                                       swapRB=False)
    
          #Predict Gender
          gender_net.setInput(blob)
          gender_preds = gender_net.forward()
          gender = self.gender_list[gender_preds[0].argmax()]
          print("Gender : " + gender)
    
          #Predict Age
          age_net.setInput(blob)
          age_preds = age_net.forward()
          age = self.age_list[age_preds[0].argmax()]
          print("Age Range: " + age)
          
          lastname= firstname + str(personcounter)
          
          self.usel.dbman.insert_person_emotion(firstname, lastname, 
                               entityid, age, gender, emotion)
    
          overlay_text = "%s %s" % (gender, age)
          cv2.putText(image, overlay_text, (x, y), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.imshow crashes in colab
          #cv2.imshow('frame', image) 
          #from google.colab.patches import cv2_imshow
          #cv2_imshow(image)
    
    #program waits up to 1 millisecond for the user to press a key. It then takes the value of the key read 
    #and ANDs it with 0xFF which removes anything above the bottom 8-bits and compares the result 
    #of that with the ASCII code for the letter q which would mean the user has decided to quit by pressing q on the keyboard.
          if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

#main procedure
#if __name__ == "__main__":
#    age_net, gender_net = load_caffe_models()
#    video_detector(age_net, gender_net)
    def video_detector2(self, image, age_net, gender_net): #, personcounter):
    
      #while True:
      #  ret1=False
      #  ret, image = self.cap.read()
      #  if (ret==False and self.cap.isOpened()==False):
      #      ret1 = self.cap.open(play.url) #da passare come param
      #  if (ret==False and ret1==False):
      #   print('Error in open video')
      
      #Load the pre-built model for facial detection
        #cascade_path= modelfullpath + 'haarcascade_frontalface_alt.xml' 
        #print(cascade_path)
      #face_cascade = cv2.CascadeClassifier(modelfullpath + 'haarcascade_frontalface_alt.xml')
      face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
     
      #OpenCV face detector expects gray images e quindi conversione in gray
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    #detect faces from an image. Params: grayscale image, scaleFactor, minNeighbors
      faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
      if (len(faces)>0):
        print("Found {} faces".format(str(len(faces))))
        personcounter = len(faces)
    
        #Loop through the list of faces and draw rectangles on the human faces
        for (x, y, w, h )in faces:
          cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
          #Get Face 
          face_img = image[y:y+h, h:h+w].copy()
          blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), self.MODEL_MEAN_VALUES, 
                                       swapRB=False)
    
          #Predict Gender
          gender_net.setInput(blob)
          gender_preds = gender_net.forward()
          gender = self.gender_list[gender_preds[0].argmax()]
          print("Gender : " + gender)
    
          #Predict Age
          age_net.setInput(blob)
          age_preds = age_net.forward()
          age = self.age_list[age_preds[0].argmax()]
          print("Age Range: " + age)
          
          lastname= self.firstname + str(personcounter)
          #age value???
          self.usel.dbman.insert_person_emotion(self.firstname, lastname, 
                               self.entityid, age, gender, self.emotion)
    
          overlay_text = "%s %s" % (gender, age)
          cv2.putText(image, overlay_text, (x, y), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.imshow crashes in colab
          #cv2.imshow('frame', image) 
          #from google.colab.patches import cv2_imshow
          #cv2_imshow(image)
    
    #program waits up to 1 millisecond for the user to press a key. It then takes the value of the key read 
    #and ANDs it with 0xFF which removes anything above the bottom 8-bits and compares the result 
    #of that with the ASCII code for the letter q which would mean the user has decided to quit by pressing q on the keyboard.
          #if cv2.waitKey(1) & 0xFF == ord('q'): 
          #  break

agegender = AgeGender()
agegender.video_detector(agegender.age_net, agegender.gender_net)