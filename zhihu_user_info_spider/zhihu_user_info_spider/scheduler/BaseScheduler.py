import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_MISSED, EVENT_JOB_ERROR
import logging

"""时刻表的父类"""


class BaseScheduler(object):
    def __init__(self, name: str):
        self.sche = BlockingScheduler()
        self.sche.add_listener(self.job_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED)
        self.sche._logger = logging
        self.job_logger = logging.getLogger(name=name)
        file_handler = logging.FileHandler(filename=os.getcwd() + os.sep + "log" + os.sep + name + ".log", mode="a",
                                           encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
        file_handler.setLevel(logging.INFO)
        self.job_logger.addHandler(file_handler)
        logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            level=logging.INFO,
                            filemode='a')

    def job_listener(self, Event):
        job = self.sche.get_job(Event.job_id)
        if not Event.exception:
            self.job_logger.info("jobname=%s|jobtrigger=%s|jobtime=%s|retval=%s", job.name, job.trigger,
                                 Event.scheduled_run_time, Event.retval)
        else:
            self.job_logger.error("jobname=%s|jobtrigger=%s|errcode=%s|exception=[%s]|traceback=[%s]|scheduled_time=%s",
                                  job.name,
                                  job.trigger, Event.code,
                                  Event.exception, Event.traceback, Event.scheduled_run_time)
