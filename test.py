__author__ = 'Chad Dotson'

from PiPy.sensor_interface import MotionDetector, RangeFinder


import threading



rf = RangeFinder(23, 24)


def notified():
    print rf.get_range()

md = MotionDetector(notified, 7)

t = threading.Thread(target=md.monitor, args=())

try:

    t.start()


except KeyboardInterrupt:
    md.active = False

t.join()
