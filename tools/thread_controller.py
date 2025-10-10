from PyQt5.QtCore import QThread, pyqtSignal
from job_manager.jobs.abt import Abt
from job_manager.jobs.cereniti import Cereniti
from job_manager.jobs.beacon import Beacon

class ThreadController(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, job_info, thread_window, browser):
        super().__init__()
        self.job_info = job_info
        self.browser = browser
        self._is_running = True 
        thread_window.thread_controller = self
        
    @property
    def is_cancelled(self):
        return not self._is_running

    def run(self):
        try:
            globals()[self.job_info['title'].title()](self.browser, self.job_info, self)
            self.finished_signal.emit()
        except Exception as e:
            print("Error in ThreadController:", e)
        finally:
            self.browser.close()

    def cancel(self):
        self._is_running = False
        self.browser.close()