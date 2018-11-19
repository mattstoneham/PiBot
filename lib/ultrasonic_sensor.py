__author__ = 'Matt'

import RPi.GPIO as GPIO
import time


class UltraSonicSensor(object):

    TRIGGER_PIN = 0
    ECHO_PIN = 0

    def __init__(self, trigger=18, echo=23):
        self.TRIGGER_PIN = trigger
        self.ECHO_PIN = echo

    def _send_trigger_pulse(self):
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.0001)
        GPIO.output(self.TRIGGER_PIN, False)

    def _wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.ECHO_PIN) != value and count > 0:
            count -= 1

    def get_distance(self):
        self._send_trigger_pulse()
        self._wait_for_echo(True, 10000)
        start = time.time()
        self._wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm