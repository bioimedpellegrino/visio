#facerec_faster_sql2.py

#INSTALL face recognition libs
#sudo pip3 install face_recognition
#packages: dlib==19.23.0, face-recognition-models==0.3.0, face-recognition==1.3.0 

#0 ogni funzione su file.py distinto
#1 recupera image da video
#2 face recognition
#3 audio in caso di riconoscimento: time_audio.py
#4 mqtt: spedisce detected_facenum a topic (=fTopic) di mqtt
#5 inserimento in sqlite detected_facenum
#5.1 add record(detected_facenum, timestamp) to table t_imagedata (db= /home/pi/lab/visio/visiodb.sqlite3, t_camera.id = 1)
#6 estendi sqlite per recognized_face
import face_recognition
import cv2
import numpy as np
import time as time
#from datetime import datetime
import pandas as pd

from time_audio import *
#from mqtt_serv import *
import sys

class FaceRecognition:
    def __init__(self):
        sys.path.insert(1, '/home/pi/visiog/procedure')
        import usersel
        self.dbman= self.usersel.Usersel().dbman
        self.portraitpath= self.dbman.portraitpath
        self.age=0
        self.gender='-'
        self.emotion='Neutral'        
        sys.path.insert(1, '/home/pi/visiog/procedure/face_recognition')
        import time_audio 
        self.audio = self.time_audio.Audio()
        
    def prepareLists(self, known_face_names, known_face_name_ids, known_face_encodings):
        
        dataframe= pd.DataFrame()
        dataframe = self.dbman.get_persons(dataframe)
        
        for row in dataframe.itertuples(): 
        #row[0]==index, row[1]== id, row[2]==firstname, row[3]==lastname, row[4]==imagepath, row[5]==imagename
            known_face_name_ids.append(row[1])
            known_face_names.append(row[2] + " " + row[3])
            print(str(row[1]) + " " + row[2] + " " + row[3] + " " + row[4])    
            #known_images.append(row['imagepath'] + row['imagename'])
            cur_image = face_recognition.load_image_file(self.portraitpath + row[4])
            cur_face_encoding = face_recognition.face_encodings(cur_image)[0]
            known_face_encodings.append(cur_face_encoding)
       
        return known_face_names, known_face_name_ids, known_face_encodings

    def facerec_fasterproc(self, frame, imgcounter,
                           known_face_names, 
                           known_face_name_ids, 
                           known_face_encodings,
                           show_frame=False):
        
        face_locations = []
        face_encodings = []
        process_this_frame = True
        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #RISOLUZIONE RIDOTTA
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            if len(face_locations)>0:
                imgcounter=imgcounter+1
            
            if len(face_locations)>0 and self.usersel.Usersel().useaudio == 1:
                self.audio.audio_msg() # se riconosce persone bisogna comporre audio personalizzato
            if len(face_locations)>0 and self.usersel.Usersel().detection == 1:
                if self.usersel.Usersel().saveimage == 1:
                    cv2.imwrite(self.dbman.imgpath + str(imgcounter)+'.jpg', frame)      
                    self.dbman.insert_imagedata(len(face_locations), str(imgcounter)+'.jpg', 
                                                self.dbman.cur_entityid)#entity!!!
                else:
                    self.dbman.insert_imagedata(len(face_locations), '-', self.dbman.cur_entityid)#entity!!!
                #IF DETECTION INSERT IN DB 
                
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
    
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    personid=known_face_name_ids[best_match_index]
                    face_names.append(name)
                    #sqlitevisio_db.add_person_entity(dbfullpath, personid, entityid)
                    self.dbman.insert_visiorecognition(personid, self.dbman.cur_entityid, self.age, 
                                                  self.gender, self.emotion) #entity!!!
    
        process_this_frame = not process_this_frame
        
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
        # Display the resulting image
        if show_frame:
            cv2.imshow('Video', frame)
        return imgcounter

##################################### NOT USED   
    def facerec_faster(self, useaudio):
        dbman= self.usersel.Usersel().dbman
        portraitpath=dbman.portraitpath #'/home/pi/visiog/pictures/portraits/'
        
        dataframe= pd.DataFrame()
        dataframe = dbman.get_persons(dataframe) #dbfullpath, dataframe
        
        print(len(dataframe.index)) #numero di righe del dataframe
        
        #GLOBAL VAR per current entityid
        entityid= dbman.cur_entityid 
        age=0
        gender='-'
        emotion='Neutral'
        
        known_face_names = []
        known_face_name_ids = []
        #known_images = []
        known_face_encodings = []
        
        #dataframe=dataframe.reset_index() dataframe.iterrows():
        for row in dataframe.itertuples(): 
            #row[0]==index, row[1]== id, row[2]==firstname, row[3]==lastname, row[4]==imagepath, row[5]==imagename
            known_face_name_ids.append(row[1])
            known_face_names.append(row[2] + " " + row[3])
            print(str(row[1]) + " " + row[2] + " " + row[3] + " " + row[4])    
            #known_images.append(row['imagepath'] + row['imagename'])
            cur_image = face_recognition.load_image_file(portraitpath + row[4])
            #if row[1] < 3:#!!!
            cur_face_encoding = face_recognition.face_encodings(cur_image)[0]
            known_face_encodings.append(cur_face_encoding)
        
        
        # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
        # other example, but it includes some basic performance tweaks to make things run a lot faster:
        #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
        #   2. Only detect faces in every other frame of video.
        
        # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
        # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
        # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
        
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        
        #imgpath="/home/pi/visio/pictures/portraits/"
        #obama="obama-240p.jpg"
        #biden="biden.jpg"
        
        # Load a sample picture and learn how to recognize it.
        #obama_image = face_recognition.load_image_file(imgpath+obama)
        #obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        
        # Load a second sample picture and learn how to recognize it.
        #biden_image = face_recognition.load_image_file(imgpath+biden)
        #biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        
        # Create arrays of known face encodings and their names
        ##known_face_encodings = [obama_face_encoding, biden_face_encoding]
        
        ##known_face_names = ["Barack Obama", "Joe Biden"]
        
        # Initialize some variables
        face_locations = []
        face_encodings = []
        #face_names = []
        process_this_frame = True
        
        while True:
            time.sleep(0.04) #25 fps
            # Grab a single frame of video
            ret, frame = video_capture.read()
        
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #RISOLUZIONE RIDOTTA
        
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                if len(face_locations)>0 and useaudio:
                    audio_msg() # se riconosce persone bisogna comporre audio personalizzato
                    #IF DETECTION INSERT IN DB 
        
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
        
                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]
        
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        personid=known_face_name_ids[best_match_index]
                        face_names.append(name)
                        #sqlitevisio_db.add_person_entity(dbfullpath, personid, entityid)
                        dbman.insert_visiorecognition(personid, entityid, age, gender, emotion)
        
            process_this_frame = not process_this_frame
        
        
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
        
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
            # Display the resulting image
            cv2.imshow('Video', frame)
        
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

#useaudio= True    
#facerec_faster(usersel.Usersel().useaudio)    
