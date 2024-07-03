import logging

from robocorp.tasks import task

from src.application.apnews_robot import ApNewsRobot
from src.infrastructure.log_config import LogConfig


@task
def start():
    try:
        LogConfig()
        ApNewsRobot().start()
    except Exception as ex:
        logging.error(f" ... Error initializing application: {ex} ...")


if __name__ == "__main__":
    start()
