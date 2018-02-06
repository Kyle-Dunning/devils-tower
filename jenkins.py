import ast
import urllib.request
from enum import Enum
import logging

log = logging.getLogger()

BASE_URL = 'http://jenkins.thoughtmachine.net:8080/job/%s/api/python'


class Status(Enum):
    SUCCESS = 1
    FAILED = 2
    DISABLED = 3


def get_status_of_jobs(url, jobs):
    overal_status = Status.SUCCESS
    disabled_jobs = False
    for job in jobs:
        status = get_status_from_jenkins(url, job)
        if status is Status.FAILED:
            overal_status = status
        elif status is Status.DISABLED:
            disabled_jobs = True
    return overal_status, disabled_jobs


def get_status_from_jenkins(url, project):
    with urllib.request.urlopen(url % project) as response:
        html = response.read().decode('UTF-8')
        info = ast.literal_eval(html)
        color = info['color']

        if 'disabled' in color:
            return Status.DISABLED
        elif 'blue' in color:
            return Status.SUCCESS
        else:
            return Status.FAILED
