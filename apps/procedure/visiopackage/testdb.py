# testdb.py

import datetime
import sys
print(sys.version)

sys.path.insert(1,'/home/pi/visio/apps/procedure')
from usersel import *

dbmgr_path = r'/home/pi/visio/apps/procedure/visiopackage'
usel= Usersel(dbmgr_path)
#usel.showparams()

#CREATE POPULATE DB
#usel.createPopulateDB()

usel.detection= 1
usel.recognition= 0
usel.emotion_agegender= 1
usel.saveimage= 0
usel.useaudio= 1
usel.framelapse= 0.04

#usel.updateparams(1,1,1,0,1,0.04)

usel.setparams_2Db() #WRITE from usersel 2 DB

usel.getparams_fromDb() #READ from DB 2 Usersel

usel.showparams() #show Usersel

#usel.getvisiorecog_fromDb()

usel.getEntities_fromDb()

# sum(face_num) from  last day from now
##val = usel.getlastday_facenum()
print(str(val))

# SUM(face_num) from 2 dates (init, end)
##val = usel.get_daterange_facenum('2022-07-24', '2022-07-25')
print(str(val))

#SUM(face_num) from 2 datetimes (init,end)
end = datetime.datetime.fromisoformat('2022-07-24 23:59:59') #'2022-07-24 24:00:00'
init = datetime.datetime.fromisoformat('2022-07-24 23:44:00')

##val = usel.get_datetime_range_facenum(init, end)
print(str(val))

#face_num records avery 15 minutes 
#init = datetime.datetime.fromisoformat('2022-07-24 00:00:00')
#end = datetime.datetime.fromisoformat('2022-07-24 23:59:59')
init = '2022-07-24 00:00:00'
end = '2022-07-24 23:59:59'

time_period= 15
usel.get_period_imagedata(init, end, time_period)

# DELETE home_visiorecognition
#usel.deleteVisioRec(usel.dbman.cur_entityid)

#DELETE home_imagedata
#usel.deleteImagedata(usel.dbman.cur_entityid)

#DELETE home_persons without face_image
#usel.deletePersons()
'''
COMMON TABLE EXPRESSION
WITH cte(created, face_num) AS (
    SELECT MIN(created), face_num FROM home_imagedata 
    UNION ALL
    SELECT datetime(created, '+15 minutes'), face_num
    FROM cte
    WHERE datetime(created, '+15 minutes') < (
            SELECT MAX(created) FROM home_imagedata 
            WHERE datetime(created) BETWEEN datetime('2022-07-24 00:00:00') AND datetime('2022-07-24 23:59:59')
    ))
    SELECT created, face_num FROM cte;

Error: recursive aggregate queries not supported   
WITH cte(created, face_num) AS (
    SELECT MIN(created), SUM(face_num) FROM home_imagedata 
    UNION ALL
    SELECT datetime(created, '+15 minutes'), SUM(face_num)
    FROM cte
    WHERE datetime(created, '+15 minutes') < (
            SELECT MAX(created) FROM home_imagedata 
            WHERE datetime(created) BETWEEN datetime('2022-07-24 00:00:00') AND datetime('2022-07-24 23:59:59')
    ))
    SELECT created, face_num FROM cte; 
    
SELECT SUM(face_num) FROM home_imagedata 
WHERE datetime(created) BETWEEN datetime("2022-07-24 00:11:46") AND date("2022-07-24 00:26:46");

SELECT sum(face_num) FROM home_imagedata 
WHERE datetime(created) BETWEEN datetime('2022-07-24 17:51:00') AND datetime('2022-07-24 18:06:00');   
'''

