from front_end.base_windows.methods import Methods
from tools.thread_controller import ThreadController
from tools.browser import Browser
from functools import partial

class Jobs(Methods):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def init_ui(self, job_info):
        self.clear_layout()
        self.setWindowTitle(job_info['title'])
        self.window_info(job_info)
        self.create_button('Start', partial(self.run_job, job_info))
        self.create_button('Back', partial(self.controller.switch_window, 'main'))

    def window_info(self, job_info):
        match job_info['title']:
            case 'abt':
                self.abt_info(job_info)

    def abt_info(self, job_info):
        for title, info in job_info['info'].items():
            info['include'] = False
            checkbox = self.create_checkbox(title)
            checkbox.stateChanged.connect(
                lambda state, cb=checkbox, inf=info: inf.update({'include': cb.isChecked()})
                )
            date_input = self.create_text_input(info['import_date'], info['import_date'])
            date_input.textChanged.connect(
                lambda text, tit=title, inf=info: self.handle_date_change(text, tit, inf, job_info['title']))
            
    def run_job(self, job_info):
        self.clear_layout()
        browser = Browser()
        thread_window = self.controller.window_instances['thread']
        self.thread_controller = ThreadController(job_info, thread_window, browser)
        self.controller.switch_window('thread')
        self.thread_controller.start()
