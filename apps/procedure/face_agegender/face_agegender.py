#face_agegender
import cv2
import numpy as np
#import pafy

cap = cv2.VideoCapture(0)
#cap.set(propId, value), here 3 is the propertyId of width and 4 is for Height.
cap.set(3, 480) #set width of the frame
cap.set(4, 640) #set height of the frame

#3 separate lists for storing Model_Mean_Values, Age and Gender.
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

gender_list = ['Male', 'Female']

modelfullpath="/home/pi/visio/procs/face_agegender/agegender_model/" 
def load_caffe_models():
    age_net = cv2.dnn.readNetFromCaffe(modelfullpath + 'deploy_age.prototxt', modelfullpath +'age_net.caffemodel')
    gender_net = cv2.dnn.readNetFromCaffe(modelfullpath + 'deploy_gender.prototxt', modelfullpath + 'gender_net.caffemodel')

    return(age_net, gender_net)


def video_detector(age_net, gender_net):
  font = cv2.FONT_HERSHEY_SIMPLEX

  while True:
    ret1=False
    ret, image = cap.read()
    if (ret==False and cap.isOpened()==False):
        ret1 = cap.open(play.url) #da passare come param
    if (ret==False and ret1==False):
      print('Error in open video')
  
  #Load the pre-built model for facial detection
    cascade_path= modelfullpath + 'haarcascade_frontalface_alt.xml' 
    #print(cascade_path)
  #face_cascade = cv2.CascadeClassifier(modelfullpath + 'haarcascade_frontalface_alt.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
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
      blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

      #Predict Gender
      gender_net.setInput(blob)
      gender_preds = gender_net.forward()
      gender = gender_list[gender_preds[0].argmax()]
      print("Gender : " + gender)

      #Predict Age
      age_net.setInput(blob)
      age_preds = age_net.forward()
      age = age_list[age_preds[0].argmax()]
      print("Age Range: " + age)

      overlay_text = "%s %s" % (gender, age)
      cv2.putText(image, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.imshow crashes in colab
    #cv2.imshow('frame', image) 
      #from google.colab.patches import cv2_imshow
      cv2_imshow(image)

#program waits up to 1 millisecond for the user to press a key. It then takes the value of the key read 
#and ANDs it with 0xFF which removes anything above the bottom 8-bits and compares the result 
#of that with the ASCII code for the letter q which would mean the user has decided to quit by pressing q on the keyboard.
      if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

#main procedure
if __name__ == "__main__":
    age_net, gender_net = load_caffe_models()

    video_detector(age_net, gender_net)
