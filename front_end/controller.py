from PyQt5.QtWidgets import QStackedWidget
from front_end.windows.main import Main
from front_end.base_windows.thread import Thread
from front_end.windows.jobs import Jobs

class Controller(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.window_instances = {}
        self.init_ui()

    def init_ui(self):
        windows = ['main', 'thread', 'jobs']
        for window in windows:
            window_class = globals().get(window.title())
            instance = window_class(self)
            self.window_instances[window] = instance
            self.addWidget(instance)

        self.switch_window('main')

    def switch_window(self, window):
        self.setCurrentWidget(self.window_instances[window])

    def init_job(self, job_info):
        self.window_instances['jobs'].init_ui(job_info)
        self.switch_window('jobs')