from front_end.base_windows.methods import Methods
from job_manager.job_info import JobInfo
from functools import partial
import json


class Main(Methods):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        jobs = ['abt', 'cereniti']
        self.setWindowTitle("Utilities Tool")
        for job in jobs:
            self.create_button(job.title(), partial(self.init_job, job))

    def init_job(self, job):
        job_info = JobInfo(job).job_info
        self.controller.init_job(job_info)
