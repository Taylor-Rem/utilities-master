from PyQt5.QtCore import QThread, pyqtSignal
from job_manager.jobs.abt import Abt
from job_manager.jobs.cerenity import Cereniti

class ThreadController(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, job_info, thread_window, browser):
        super().__init__()
        self.job_info = job_info
        self.browser = browser
        self._is_running = True 
        self.setup_thread(thread_window)
        
    def setup_thread(self, thread_window):
         # Connect signals to update the thread window.
        self.progress_signal.connect(thread_window.update_progress)
        self.finished_signal.connect(thread_window.on_finished)
        thread_window.thread_controller = self

    @property
    def is_cancelled(self):
        return not self._is_running

    def run(self):
        try:
            globals()[self.job_info['title'].title()](self.browser, self.job_info, self)
            self.finished_signal.emit()
            self.browser.close()
        except Exception as e:
            print("Error in ThreadController:", e)
        finally:
            self.browser.close()

    def cancel(self):
        self._is_running = False
        self.browser.close()