from enum import Enum
import time

from third_party.absl import logging


# BCM gpio ports
class Light(Enum):
    RED = 17
    YELLOW = 27
    GREEN = 22


class State(Enum):
    ON = 1
    OFF = 2


class TrafficLights(object):
    def on(self, light):
        logging.info('%s turned on', light)

    def off(self, light):
        logging.info('%s turned off', light)

    def all_on(self):
        for light in Light:
            self.on(light)

    def all_off(self):
        for light in Light:
            self.off(light)

    def green_only(self):
        self.all_off()
        self.on(Light.GREEN)

    def yellow_only(self):
        self.all_off()
        self.on(Light.YELLOW)

    def red_only(self):
        self.all_off()
        self.on(Light.RED)

    def blink(self, light, x, duration=0.1):
        for _ in range(x):
            self.on(light)
            time.sleep(duration)
            self.off(light)
            time.sleep(duration/2)

    def blink_green(self, x):
        self.blink(Light.GREEN, x)

    def blink_yellow(self, x):
        self.blink(Light.YELLOW, x)

    def blink_red(self, x):
        self.blink(Light.RED, x)
