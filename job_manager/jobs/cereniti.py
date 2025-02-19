from config import cereniti_username, cereniti_password
from job_manager.jobs.jobs_base import JobsBase
from resmap_ops.resmap_import import ResmapImport
from selenium.webdriver.common.by import By
import os, time

class Cereniti(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        self.run_job()

    def run_job(self):
        self.download_from_cereniti()
        for value in self.job_info['info'].values():
            pass
            # ResmapImport(self.browser, self.thread).import_file(value['propid'], value['dropdowns'], value['file_path'])
            
    def download_from_cereniti(self):
        self.browser.driver.get(self.job_info['cereniti_url'])
        self.login()
        self.browser.wait_for_page_load()
        rows = self.define_rows()
        idx = 0
        while idx < len(rows):
            if self.cancelled():
                return
            value = list(self.job_info['info'].values())[idx]
            if not value['include'] or os.path.exists(value['file_path']):
                idx += 1
                continue
            row = rows[idx]
            row.click()
            self.browser.driver.execute_script("ConsumersList();")
            self.browser.wait_for_page_load()
            self.browser.driver.execute_script("ExportReadings();")
            time.sleep(1)
            self.browser.wait_for_downloads()
            os.rename(value['file_path'], value['adjusted_file_path'])
            self.browser.switch_to_primary_tab()
            self.browser.driver.get(self.job_info['cereniti_url'])
            self.browser.wait_for_page_load()
            rows = self.define_rows()
            idx += 1

    def define_rows(self):
        property_table = self.browser.wait_for_presence_of_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/div[3]/table/tbody/tr/td[1]/div/div[2]/table/tbody')
        return property_table.find_elements(By.XPATH, ".//tr")
    
    def login(self):
        try:
            self.browser.wait_for_presence_of_element(By.NAME, 'userid')
            self.browser.send_keys(By.NAME, 'userid', cereniti_username)
            self.browser.send_keys(By.NAME, 'password', cereniti_password, True)
        except:
            pass

