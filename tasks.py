import logging

from robocorp.tasks import task

from src.application.apnews_robot import ApNewsRobot


@task
def start():
    try:
        ApNewsRobot().start()
    except Exception as ex:
        logging.error(f"Error initializing application: {ex}")


if __name__ == "__main__":
    start()
