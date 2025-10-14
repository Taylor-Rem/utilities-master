from tools.thread_controller import ThreadController
from front_end.windows.job_methods import JobMethods
from tools.browser import Browser
from functools import partial

class Jobs(JobMethods):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def init_ui(self, job_info):
        self.clear_layout()
        self.setWindowTitle(job_info['title'])
        self.set_job_info(job_info)
        self.create_button('Start', partial(self.run_job, job_info))
        self.create_button('Back', partial(self.controller.switch_window, 'main'))

    def run_job(self, job_info):
        self.pre_job_ops(job_info)
        self.clear_layout()
        browser = Browser()
        thread_window = self.controller.window_instances['thread']
        self.thread_controller = ThreadController(job_info, thread_window, browser)
        self.thread_controller.finished_signal.connect(lambda: self.controller.switch_window('main'))
        self.controller.switch_window('thread')
        self.thread_controller.start()

    def pre_job_ops(self, job_info):
        job_info['info'] = list(filter(lambda val: val['include'], job_info['info']))
        for value in job_info['info']:
            value['adjusted_file_path'] = f"{value['adjusted_file_path']}_{value['import_date']}.csv"
            if job_info['title'] == "abt": value['file_path'] = f"{value['file_path']} {value['import_date_obj'].toString('MM_dd_yyyy')}.csv"
