from selenium.webdriver.common.by import By
from job_manager.jobs.jobs_base import JobsBase
from resmap_ops.resmap_import import ResmapImport
import os, time

class Abt(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        self.resmap_import = ResmapImport(browser, thread)
        self.run_job()

    def run_job(self):
        for value in self.job_info['info']:
            if not value['include']:
                continue
            if not os.path.exists(value['file_path']):
                self.download_from_abt(value)
            if self.cancelled():
                return
        for value in self.job_info['info']:
            if not value['include']:
                continue
            if self.cancelled():
                return
            self.resmap_import.import_file(value['propid'], value['dropdowns'], value['file_path'])
        time.sleep(3)

    def download_from_abt(self, value):
        self.browser.driver.get(value['abt_url'])
        self.browser.wait_for_presence_of_element(By.XPATH, '//input[@type="submit" and @value="Export a Readings File"]')
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Export a Readings File"]')
        self.browser.wait_for_presence_of_element(By.XPATH, '//input[@type="TEXT" and @name="The Date"]')
        self.browser.send_keys(By.XPATH, '//input[@type="TEXT" and @name="The Date"]', value['import_date'])
        self.browser.find_select(By.NAME, 'ExportFormat', 'Starnik')
        if self.cancelled():
            return
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Go!"]')
