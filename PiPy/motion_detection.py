__author__ = 'Chad Dotson'


import RPi.GPIO as GPIO
import time


class MotionDetector
    _callback = None

    _current_state = 0
    _previous_state = 0

    _gpio_input = None

    active = True

    def __init__(self, callback, gpio_input):
        self._callback = callback
        self._gpio_input = gpio_input

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._gpio_input, GPIO.IN)
        while GPIO.input(self._gpio_input) == 1:
            self._current_state = 0

    def __del__(self):
        GPIO.cleanup()

    def monitor(self):

        self._current_state = GPIO.input(self._gpio_input)

        if self._current_state == 1 and self._previous_state == 0:
            self._notify()
            self._previous_state = 1

        elif self._current_state == 0 and self._previous_state == 1:
            self._previous_state = 0

        time.sleep(0.01)

    def _notify(self):
        self._callback()

