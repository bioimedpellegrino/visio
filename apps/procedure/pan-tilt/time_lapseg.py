'''
    Time-lapse photography based on the Raspistill command
'''
from time import perf_counter, sleep,strftime,localtime
#from vilib import Vilib
from sunfounder_io import PWM,Servo,I2C
import cv2
import os
import sys
import tty
import termios
import threading
#import pty

class PanTilt:
    def __init__(self):
        self.manual = '''
#                    Press keys on keyboard to record value!
                        W: up
                        A: left
                        S: down
                        D: right
                        Q: start Time-lapse photography 
                        E: stop
                        G: Quit
                    '''
        self.I2C = I2C().reset_mcu()
        self.sleep = sleep(0.01)
        self.pan = Servo(PWM("P0"))
        self.tilt = Servo(PWM("P1"))
        self.panAngle = 0
        self.tiltAngle = 0
        self.pan.angle(self.panAngle)
        self.tilt.angle(self.tiltAngle)
        self.key = None
        self.breakout_flag=False
        
# region  read keyboard 
    def readchar(self):
        fd = sys.stdin.fileno()
        #pid = pty.fork()
        #if not pid:
    # is child
            #termios.tcgetattr(sys.stdin.fileno())
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# endregion

# region init
#I2C().reset_mcu()
#sleep(0.01)

#pan = Servo(PWM("P0"))
#tilt = Servo(PWM("P1"))
#panAngle = 0
#tiltAngle = 0
#pan.angle(panAngle)
#tilt.angle(tiltAngle)

# endregion

# # check dir 
    def check_dir(self,dir):
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception as e:
                print(e)

# region servo control
    def limit(self,x,min,max):
        if x > max:
            return max
        elif x < min:
            return min
        else:
            return x

    def servo_control(self,key):
        #global panAngle,tiltAngle       
        if key == 'w':
            self.tiltAngle -= 1
            self.tiltAngle = self.limit(self.tiltAngle, -90, 90)
            self.tilt.angle(self.tiltAngle)
        if key == 's':
            self.tiltAngle += 1
            self.tiltAngle = self.limit(self.tiltAngle, -90, 90)
            self.tilt.angle(self.tiltAngle)
        if key == 'a':
            self.panAngle += 1
            self.panAngle = self.limit(self.panAngle, -90, 90)
            self.pan.angle(self.panAngle)
        if key == 'd':
            self.panAngle -= 1
            self.panAngle = self.limit(self.panAngle, -90, 90)
            self.pan.angle(self.panAngle)

# endregion servo control

# Video synthesis
    def video_synthesis(self,name:str,input:str,output:str,fps=30,format='.jpg',datetime=False):
    
        print('processing video, please wait ....')
    
        # video parameter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output+'/'+name, fourcc, fps, (640,480))
        width = 640
        height = 480
    
        # traverse   
        for root, dirs, files in os.walk(input):
            print('%s pictures be processed'%len(files))
            files = sorted(files)
            for file in files:
                # print('Format:',os.path.splitext(file)[1])
                if os.path.splitext(file)[1] == format:
                    # imread
                    frame = cv2.imread(input+'/'+file)
                    # add datetime watermark
                    if datetime == True:
                        # print('name:',os.path.splitext(file)[1])
                        time = os.path.splitext(file)[0].split('-')
                        year = time[0]
                        month = time[1]
                        day = time[2]
                        hour = time[3]
                        minute = time[4]
                        second = time[5]
                        frame = cv2.putText(frame, 
                                            '%s.%s.%s %s:%s:%s'%(year,month,day,hour,minute,second),
                                            (width - 180, height - 25), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 255, 255),
                                            1, 
                                            cv2.LINE_AA)   # anti-aliasing
                    # write video
                    out.write(frame)
    
        # release the VideoWriter object
        out.release()
    
        # remove photos
        os.system('sudo rm -r %s'%input)
        print('Done.The video save as %s/%s'%(output,name))

# keyboard scan thread
#key = None
#breakout_flag=False
    def keyboard_scan(self):
        #global key
        while True:
            self.key = None
            self.key = self.readchar()
            sleep(0.01)
            if self.breakout_flag==True: #'g'
                break
        
# continuous_shooting
    def continuous_shooting(self,path,interval_ms:int=3000):
        print('Start time-lapse photography, press the "e" key to stop')   
    
        delay = 10 # ms    
        count = 0
        while True:    
            if count == interval_ms/delay:
                count = 0
                Vilib.take_photo(photo_name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),path=path)
            if self.key == 'e':
                break
            count += 1
            sleep(delay/1000) # second


# main
    def main(self):  
        print(self.manual)
    ##    Vilib.camera_start(vflip=True,hflip=True)
    ##    Vilib.display(local=True,web=True)
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
    
    ##    sleep(1)
        t = threading.Thread(target=self.keyboard_scan)
        t.setDaemon(True)
        t.start()
                
        while True:
            __, frame = cap.read()
            
            self.servo_control(self.key)
    
            # time-lapse photography
            if self.key == 'q':    
                #check path
                output = "/home/pi/visio/Pictures/time_lapse" # -o
                input = output+'/'+strftime("%Y-%m-%d-%H-%M-%S", localtime())
                self.check_dir(input)
                self.check_dir(output)
    
                # take_photo
    ##            continuous_shooting(input,interval_ms=3000)
                
                # video_synthesis
                #name=strftime("%Y-%m-%d-%H-%M-%S", localtime())+'.avi'
    ##            video_synthesis(name=name,input=input,output=output,fps=30,format='.jpg',datetime=True)
                
            # esc
            if self.key == 'g':
    ##            Vilib.camera_close()
                global breakout_flag
                breakout_flag=True
                sleep(0.1)
                print('The program ends, please press CTRL+C to exit.')
                break 
            sleep(0.01)
            
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) &0xFF == ord('r'):
                break
            
        #When everything's done, release capture
        cap.release()
        cv2.destroyAllWindows()

#if __name__ == "__main__":
#    main()
pantilt = PanTilt()
pantilt.main()
