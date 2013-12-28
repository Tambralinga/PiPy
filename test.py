__author__ = 'Chad Dotson'

from PiPy.sensor_interface import MotionDetector, RangeFinder

import picamera
import threading

#from settings import Settings

import time

rf = RangeFinder(23, 24)



i = 0


from os.path import join
from os import mkdir
from datetime import datetime


class MotionEventHandler:

    def __init__(self, base_directory):
        self._base_directory = base_directory
        self._current_index = 0
        self._current_subdirectory = None
        self._is_capturing = False
        self._last_capture = None

        self._camera = picamera.PiCamera()

    def capture(self):
        if not self.is_capturing():
            self.start_capturing()

        self._last_capture = datetime.now()

        self._camera.capture(join(self._base_directory, self._current_subdirectory, str(self._current_index) + ".jpg"),
                             'jpeg', quality=95)

        self._current_index += 1

    def is_capturing(self):
        if self._last_capture is None or (datetime.now() - self._last_capture).seconds > 5:
            return False
        return True

    def start_capturing(self):
        self._current_index = 0
        self._current_subdirectory = time.strftime("%Y_%m_%d_%H:%M:%S")
        mkdir(join(self._base_directory, self._current_subdirectory))


meh = MotionEventHandler("captures")
#
#def notified():
#    print rf.get_range()
#
#    global i
#    camera.capture("captures/captured_" + str(i) + ".jpg", 'jpeg', quality=95)
#
#    i += 1

md = MotionDetector(meh.capture, 7, delay=5)

t = threading.Thread(target=md.monitor, args=())

try:

    t.start()

    while t.isAlive():
        time.sleep(1)


except KeyboardInterrupt:
    md.active = False

finally:
    GPIO.cleanup()


