__author__ = 'Chad Dotson'


import RPi.GPIO as GPIO
import time

import threading


class MotionDetector(threading.Thread):
    _callback = None

    _current_state = 0
    _previous_state = 0

    _gpio_input = None

    active = True

    def __init__(self, callback, gpio_input):
        self._callback = callback
        self._gpio_input = gpio_input

        GPIO.setup(self._gpio_input, GPIO.IN)
        while GPIO.input(self._gpio_input) == 1:
            self._current_state = 0

        super(threading.Thread, self).__init__(target= self._monitor, args = ())

    def __del__(self):
        GPIO.cleanup()

    def _monitor(self):

        while active:

            self._current_state = GPIO.input(self._gpio_input)

            if self._current_state == 1 and self._previous_state == 0:
                print "Motion Detected"
                self._previous_state = 1

            elif self._current_state == 0 and self._previous_state == 1:
                self._previous_state = 0

            time.sleep(0.01)

    def notify(self):
        self._callback()

