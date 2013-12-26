__author__ = 'Chad Dotson'

from PiPy.sensor_interface import MotionDetector, RangeFinder

import picamera
import threading

import time

rf = RangeFinder(23, 24)

camera = picamera.PiCamera()

i = 0


def notified():
    print rf.get_range()

    global i
    camera.capture("captures/captured_" + str(i) + ".jpg", 'jpeg', quality=95)

    i += 1

md = MotionDetector(notified, 7)

t = threading.Thread(target=md.monitor, args=())

try:

    t.start()

    while t.isAlive():
        time.sleep(1)


except KeyboardInterrupt:
    md.active = False


