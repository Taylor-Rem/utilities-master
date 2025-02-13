from selenium.webdriver.common.by import By
from resmap_ops.resmap_import import ResmapImport
import os

class Abt:
    def __init__(self, browser, job_info, thread):
        self.browser = browser
        self.thread = thread
        self.resmap_import = ResmapImport(browser, thread)
        self.login_info = job_info['login_info']
        self.run_job(job_info)

    def run_job(self, job_info):
        for value in job_info['info'].values():
            if self.thread.is_cancelled:
                break
            if not value['include']:
                continue

            if not os.path.exists(value['file_path']):
                self.download_from_abt(value)

            if self.thread.is_cancelled:
                break
            # self.upload_to_manage_portal(value)
            self.resmap_import.import_file(value['kmc_url'], value['dropdowns'], value['file_path'])

    def download_from_abt(self, property):
        self.browser.driver.get(property['abt_url'])
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Export a Readings File"]')
        self.browser.send_keys(By.XPATH, '//input[@type="TEXT" and @name="The Date"]', property['import_date'])
        self.browser.find_select(By.NAME, 'ExportFormat', 'Starnik')
        if self.thread.is_cancelled:
            return
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Go!"]')
