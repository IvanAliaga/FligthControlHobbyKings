import threading
import time
from gps import *

class GpsPoller(threading.Thread):

   def __init__(self):
       threading.Thread.__init__(self)
       self.session = gps(mode=WATCH_ENABLE)
       self.current_value = None
       self.latitud_value = None

   def get_current_value(self):
       return self.current_value
   
   def get_session(self):
       return self.session

   def run(self):
       try:
            while True:
                self.current_value = self.session.next()
		time.sleep(0.2) # tune this, you might not get values that quickly
       except StopIteration:
            pass
