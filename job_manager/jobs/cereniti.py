from config import cereniti_username, cereniti_password
from job_manager.jobs.jobs_base import JobsBase
from file_manager.csv_manager import CsvManager
from resmap_ops.resmap_import import ResmapImport
from selenium.webdriver.common.by import By
import os, time

class Cereniti(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        self.resmap_import = ResmapImport(browser, thread)
        self.define_rows = lambda: (self.login(), self.browser.define_rows(By.XPATH, '/html/body/table/tbody/tr/td[2]/div[3]/table/tbody/tr/td[1]/div/div[2]/table/tbody'))[1]
        self.run_job()

    def run_job(self):
        self.download_from_cereniti()
        for value in self.job_info['info']:
            if value['include']:
                self.resmap_import.import_file(value['propid'], value['dropdowns'], value['adjusted_file_path'], value['import_date'])
        time.sleep(3)
            
    def download_from_cereniti(self):
        # Check if files are downloaded already
        if len([item for item in self.job_info['info'] if not os.path.exists(item['adjusted_file_path'])]) < 1:
            # Modify files
            for value in self.job_info['info']:
                self.modify_pdf(value)
            return
        rows = self.define_rows()
        idx = 0
        while idx < len(rows):
            if self.cancelled():
                return
            value = self.job_info['info'][idx]
            if not value['include'] or os.path.exists(value['adjusted_file_path']):
                idx += 1
                continue
            self.download_file(value, rows[idx])
            self.modify_pdf(value)
            if (idx + 1 == len(rows)):
                break
            rows = self.define_rows()
            idx += 1
        self.browser.close_all_tabs_except_primary()

    def download_file(self, value, row):
        row.click()
        self.browser.driver.execute_script("ConsumersList();")
        self.browser.wait_for_page_load()
        self.browser.send_keys(By.NAME, "toDate", value['import_date'])
        self.browser.driver.execute_script("ExportReadings();")
        self.browser.wait_for_file_count_increase()
        os.rename(value['file_path'], value['adjusted_file_path'])
        self.browser.switch_to_primary_tab()

    def modify_pdf(self, value):
        csv_manager = CsvManager(value['adjusted_file_path'])
        match value['propid']:
            # Sherwood
            case 3:
                csv_manager.replace_unit_columns([{'start': 1, 'end': 121}])
            # Westcrest
            case 18:
                csv_manager.replace_unit_columns([{'start': 1, 'end': 47},{'start': 101, 'end': 147},{'start': 201, 'end': 232},{'start': 237, 'end': 260},{'start': 265, 'end': 276},{'start': 1001, 'end': 1093}])

        csv_manager.convert_units()
        csv_manager.delete_empty_rows()
        csv_manager.save_csv()

    def login(self):
        self.browser.driver.get(self.job_info['cereniti_url'])
        self.browser.wait_send_keys(By.NAME, 'userid', cereniti_username)
        self.browser.wait_send_keys(By.NAME, 'password', cereniti_password, "enter")