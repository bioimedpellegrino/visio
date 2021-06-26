from django.core.management.base import BaseCommand, CommandError
from core.models import TCamera, TImage

class Command(BaseCommand):

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        camera = TCamera.objects.get(pk=1)
        #parametri mqtt
        mqtt_broker= "localhost" #broker ‘localhost’
        #mqtt_broker= "aspoto.dyndns.org"
        topic_name = "fTopic"

        #mqtt publish
        from paho.mqtt.client import Client
        client = Client("Publisher_test")
        def on_publish(client, userdata, mid):
         print("Messaggio pubblicato")
        client.on_publish = on_publish
        client.connect(mqtt_broker) 

        client.loop_start()
        #messaggio = input("Inserisci il testo da inviare al topic test")
        #face_num =4 #from mtcnn
        #client.publish(topic = "fTopic", payload = face_num) #payload = messaggio
        #client.loop_stop()
        #client.disconnect() 

        #mtcnn on video
        import cv2
        from mtcnn_cv2 import MTCNN
        import time

        #parametri mtcnn
        threshold=0.87

        detector = MTCNN()
        #print(type(detector))

        #test
        #imshow funziona su debian con UI!
        #test_pic = "test1.jpg"
        #test_ris="face_detected.jpg"

        #image=cv2.imgread(test_pic)
        #image = cv2.cvtColor(cv2.imread(test_pic), cv2.COLOR_BGR2RGB)
        cap=cv2.VideoCapture(0)
        while True:
            #capture frame by frame
            time.sleep(0.02)
            __, frame=cap.read()
            
            i=0
            result = detector.detect_faces(frame)
            print(len(result))
            if result != []:
                    for person in result:
                        print(person['confidence'])
                        if(person['confidence']>threshold):
                            i=i+1
                            bounding_box=person['box']
                            keypoints=person['keypoints']
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
                    
                    #if i>0:
                    face_num =i 
                    client.publish(topic = topic_name, payload = face_num)
                    #sqlite
                    if i>0:
                      print(face_num)
                      t_image = TImage()
                      t_image.face_num = face_num
                      t_image.camera = camera
                      t_image.save()


            #cv2.imshow('frame', frame) #corretto in debian con UI
            if cv2.waitKey(1) & 0xFF == ord('q'): #stop digitando 1
                break
        
        #when everything done, release
        cap.release()
        cv2.destroyAllWindows()
        #mqtt stop
        client.loop_stop()
        client.disconnect()
