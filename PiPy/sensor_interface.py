__author__ = 'Chad Dotson'


import RPi.GPIO as GPIO
import time


class MotionDetector:
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
        while self.active:

            self._current_state = GPIO.input(self._gpio_input)

            if self._current_state == 1:
                self._notify()
                self._current_state = 0

            #if self._current_state == 1 and self._previous_state == 0:
            #    self._notify()
            #    self._previous_state = 1
            #
            #elif self._current_state == 0 and self._previous_state == 1:
            #    self._previous_state = 0

            time.sleep(0.01)

    def _notify(self):
        self._callback()


class RangeFinder:

    _gpio_trigger = None
    _gpio_echo = None

    def __init__(self, gpio_trigger, gpio_echo):
        self._gpio_trigger = gpio_trigger
        self._gpio_echo = gpio_echo


        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._gpio_trigger, GPIO.OUT)
        GPIO.setup(self._gpio_echo, GPIO.IN)


        GPIO.output(self._gpio_trigger, False)

        time.sleep(0.001)


    def __del__(self):
        GPIO.cleanup()

    def get_range(self):
        GPIO.output(self._gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self._gpio_trigger, False)
        start = time.time()

        while GPIO.input(self._gpio_echo) == 0:
            start = time.time()

        while GPIO.input(self._gpio_echo) == 1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = distance / 2

        return distance

