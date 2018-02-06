import sys

from third_party.absl import app
from third_party.absl import flags
from third_party.absl import logging

import time
from mock_trafficlight import TrafficLights
from mock_trafficlight import Light
from jenkins import get_status_of_jobs, Status
from datetime import datetime

import random

FLAGS = flags.FLAGS

flags.DEFINE_string('jenkins_url', None, 'Jenkins URL')
flags.DEFINE_list('build_jobs', None, 'Build jobs.')
flags.DEFINE_list('test_jobs', None, 'Test jobs.')


def get_random_state():
    num = random.randint(0, 7)
    return num & 1 != 0, num & 2 != 0, num & 4 != 0


def main(argv):
    traffic_light = TrafficLights()
    del argv

    logging.info('Initializing traffic light')
    traffic_light.all_off()

    def display_result(result, disabled_jobs):
        if result is Status.SUCCESS:
            switch_light(Light.GREEN, disabled_jobs)
        else:
            switch_light(Light.RED, disabled_jobs)

    def switch_light(light, blink):
        traffic_light.all_off()
        if blink:
            traffic_light.blink(light, 4, 1)
        else:
            traffic_light.on(light)
        time.sleep(5)

    def monitor():
        traffic_light.yellow_only()
        t = time.perf_counter()
        builds, builds_disabled = get_status_of_jobs(FLAGS.jenkins_url, FLAGS.build_jobs)
        logging.info('Builds: {}, Disabled: {}'.format(builds.name, builds_disabled))
        tests, tests_disabled = get_status_of_jobs(FLAGS.jenkins_url, FLAGS.test_jobs)
        logging.info('Tests: {}, Disabled: {}'.format(builds.name, builds_disabled))
        logging.info('Took: {}'.format(time.perf_counter()-t))

        for _ in range(3):
            display_result(builds, builds_disabled)
            traffic_light.all_off()
            time.sleep(2)
            display_result(tests, tests_disabled)
            traffic_light.yellow_only()
            time.sleep(2)

    def party():
        now = datetime.now()
        while (now.weekday() == 4 and 16 <= now.hour <= 21):
            for _ in range(10000):
                r, y, g = get_random_state()
                traffic_light.on(Light.RED) if r else traffic_light.off(Light.RED)
                traffic_light.on(Light.YELLOW) if y else traffic_light.off(Light.YELLOW)
                traffic_light.on(Light.GREEN) if g else traffic_light.off(Light.GREEN)
            now = datetime.now()

    while True:
        try:
            party()
            monitor()
        except Exception:
            logging.exception("Something bad happened, let people know I'm in trouble")
            traffic_light.all_on()


if __name__ == '__main__':
    app.run(main)
