import logging
import json

from abc import ABC, abstractmethod
from selinon import run_flow
from f8a_worker.setup_celery import init_celery

logger = logging.getLogger('Monitor')


class Backend(ABC):

    @abstractmethod
    def notify(self, notification_string):
        pass


class LoggerBackend(Backend):

    def __init__(self):
        logger.info('Using logger backend')

    def notify(self, notification_string):
        logger.info(notification_string)


SELINON_FLOW_NAME = 'golangCVEPredictionsFlow'


class SelinonBackend(Backend):

    def __init__(self):
        pass

    def notify(self, notification_string):
        init_celery(result_backend=False)
        run_flow(SELINON_FLOW_NAME, notification_string)


def create_pr_notification(package, repository, id):
    notification_dict = {
        "repository": repository,
        "package": package,
        "event": "pull-request",
        "id": id
    }
    return json.dumps(notification_dict)


def create_issue_notification(package, repository, id):
    notification_dict = {
        "repository": repository,
        "package": package,
        "event": "issue",
        "id": id
    }
    return json.dumps(notification_dict)


def create_push_notification(package, repository):
    notification_dict = {
        "repository": repository,
        "package": package,
        "event": "push",
    }
    return json.dumps(notification_dict)
