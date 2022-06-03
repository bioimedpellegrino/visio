#time_audio.py
#AUDIO
#sudo pip3 install pyalsaaudio

import sys
import wave
import getopt
import alsaaudio
from datetime import datetime

class Audio:
    def __init__(self):
        sys.path.insert(1,'/home/pi/visio/procedure')
        import self.usersel
        self.dbman= self.usersel.Usersel().dbman
        self.wave_folder= self.dbman.soundpath #'/home/pi/visio/sound/'
        self.wave_file_morn = 'buongiorno.wav'#'Nirvana2.wav'
        self.wave_file_after= 'buonpome.wav'
        self.wave_file_even= 'buonasera.wav'
        
    def play(self, device, f):   
    	format = None
    
    	# 8bit is unsigned in wav files
    	if f.getsampwidth() == 1:
    		format = alsaaudio.PCM_FORMAT_U8
    	# Otherwise we assume signed data, little endian
    	elif f.getsampwidth() == 2:
    		format = alsaaudio.PCM_FORMAT_S16_LE
    	elif f.getsampwidth() == 3:
    		format = alsaaudio.PCM_FORMAT_S24_3LE
    	elif f.getsampwidth() == 4:
    		format = alsaaudio.PCM_FORMAT_S32_LE
    	else:
    		raise ValueError('Unsupported format')
    
    	periodsize = f.getframerate() // 8
    
    	print('%d channels, %d sampling rate, format %d, periodsize %d\n' % (f.getnchannels(),
    									f.getframerate(),
    									format,
    									periodsize))
    
    	device = alsaaudio.PCM(channels=f.getnchannels(), rate=f.getframerate(), format=format, periodsize=periodsize, device=device)
    	
    	data = f.readframes(periodsize)
    	while data:
    		# Read data from stdin
    		device.write(data)
    		data = f.readframes(periodsize)

    def usage(self):
    	print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
    	sys.exit(2)
    
    def audio_msg(self):
        device = 'default'
        
        dat=datetime.now()
        print(dat.hour)
    
        hour=dat.hour
    
        if hour<=12 & hour>=0:
          fullpath= self.wave_folder + self.wave_file_morn #morning
        elif hour>12 & hour<=18:
          fullpath= self.wave_folder + self.wave_file_after #afternoon
        else:
          fullpath= self.wave_folder + self.wave_file_even #evening
    
        with wave.open(fullpath, 'rb') as f:
            play(device, f)
