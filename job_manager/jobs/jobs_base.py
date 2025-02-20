from tools.browser import Browser

class JobsBase:
    def __init__(self, browser, job_info, thread):
        self.browser = browser
        self.thread = thread
        self.job_info = job_info
        self.cancelled = lambda: self.thread.is_cancelled