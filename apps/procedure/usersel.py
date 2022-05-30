#usersel.py

import pandas as pd
import sys

#gui SAVE imposta i parametri di Usersel e chiama setparams_2Db()
#gui READ getparams_fromDb, set param values in controls
class Usersel:
    def __init__(self):
        self.id = 1
        self.detection= 0
        self.recognition= 0
        self.emotion_agegender= 0 #self.agegender= 0
        self.saveimage= 0
        self.useaudio= 0
        self.framelapse=0.04 #++
        sys.path.insert(1,'/home/pi/visiog/procwdure/visiopackage')
        import djangosqlite_db
        self.djangosqlite_db = djangosqlite_db
        self.dbman= self.djangosqlite_db.Dbmgr()
        
    def createPopulateDB(self):
        self.dbman.createDB()
        self.dbman.populateDB()
        
    def getparams_fromDb(self):  
        dataframe= pd.DataFrame()
        dataframe = self.dbman.get_params(dataframe, self.id)
        for row in dataframe.itertuples():
            #row[1]==id, row[2]=='facedetection', row[3]=='facerecognition', 
            #row[4]=='facemotion', row[5]=='faceagegender', row[6]=='saveimage', row[7]=='useaudio'])
            self.detection= row[2]
            self.recognition= row[3]
            self.emotion_agegender= row[4]
            #self.faceagegender= row[5]
            self.saveimage= row[5]
            self.useaudio= row[6]
            self.framelapse = row[7]

    def getvisiorecog_fromDb(self):  
        dataframe= pd.DataFrame()
        dataframe = self.dbman.get_visiorecognitions(dataframe)
        for row in dataframe.itertuples():
            #columns=['id','person','entity', 'age', 'gender', 'emotion', 'date'] 
            print('id= ' + str(row[1]) + ', personid= ' + str(row[2]) +
                  ', entityid= ' + str(row[3]) + ', age= ' + str(row[4]) +
                  ', gender= ' + str(row[5]) + ', emotion= ' + str(row[6]) +
                  ', date= ' + str(row[7]))
                    
    #save usersel params 2 db    
    def setparams_2Db(self): 
        self.dbman.update_params(self.id, self.detection, 
                                 self.recognition, 
                                 self.emotion_agegender, 
                                 self.saveimage, 
                                 self.useaudio,
                                 self.framelapse)
        
    #update usersel params and save them 2 db    
    def updateparams(self, detection, recognition, emotion_agegender,
                     saveimage, useaudio, framelapse):
        self.detection= detection
        self.recognition= recognition
        self.emotion_agegender= emotion_agegender #self.agegender= 0
        self.saveimage= saveimage
        self.useaudio= useaudio
        self.framelapse= framelapse
        self.setparams_2Db()
        
    def showparams(self):
        print('detection= ' + str(self.detection))
        print('recognition= ' + str(self.recognition))
        print('emotion_agegender= ' + str(self.emotion_agegender))
        #print('faceagegender= ' + str(self.faceagegender))
        print('saveimage= ' + str(self.saveimage))
        print('useaudio= ' + str(self.useaudio))
        print('framelapse= ' + str(self.framelapse))
        
    def deleteVisioRec(self, entityid):
        self.dbman.deleteVisioRec(entityid)       