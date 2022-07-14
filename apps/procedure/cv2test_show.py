import sys
import cv2

class Main():
	def __init__(self, userselection):
		userselection['detection'] = 0
		userselection['recognition'] = 0
		userselection['emotion_agegender'] = 0
		userselection['show_frame'] = 0
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
		
		'''sys.path.insert(1, '/home/pi/visio/apps/procedure/face_emotion')
		#import testextract
		#self.faceemotion = testextract.FaceEmotion(self.usel)
		'''
		sys.path.insert(1, '/home/pi/visio/apps/procedure/face_agegender')
		import face_agegender
		#self.agegender=face_agegender.AgeGender(self.usel)
		

	def mainfun(self):
		cap = cv2.VideoCapture(0)

# Capture frame
		while True:
			ret, frame = cap.read()
			if ret:
				#cv2.imwrite('image.jpg', frame)
				cv2.imshow('frame',frame)
			if cv2.waitKey(1) &0xFF == ord('q'):
				break
		cap.release()
		cv2.destroyAllWindows()

userselection = {}
main= Main(userselection)
main.mainfun()