# testdb.py
import sys
print(sys.version)

sys.path.insert(1,'/home/pi/visiog/procedure')
from usersel import *

usel= Usersel()
#usel.showparams()

#CREATE POPULATE DB
#usel.createPopulateDB()

usel.detection= 1
usel.recognition= 0
usel.emotion_agegender= 1
#usel.faceagegender= 1
usel.saveimage= 1
usel.useaudio= 1
usel.framelapse= 0.04

usel.updateparams(1,1,1,0,1,0.04)

usel.setparams_2Db() #WRITE from usersel 2 DB

usel.getparams_fromDb() #READ from DB 2 Usersel

usel.showparams() #show Usersel

usel.getvisiorecog_fromDb()

usel.getEntities_fromDb()

# DELETE home_visiorecognition
usel.deleteVisioRec(usel.dbman.cur_entityid)


