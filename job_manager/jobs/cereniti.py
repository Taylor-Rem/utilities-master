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
        self.run_job()

    def run_job(self):
        if any(not os.path.exists(value['adjusted_file_path']) for value in self.job_info['info']):
            self.login()
            self.download_from_cereniti()
        for value in self.job_info['info']:
            if value['include']:
                self.resmap_import.import_file(value['propid'], value['dropdowns'], value['adjusted_file_path'], value['import_date'])
        time.sleep(3)
            
    def download_from_cereniti(self):
        for val in self.job_info['info']:
            try:
                os.remove(val['file_path'])
            except:
                pass
            if os.path.exists(val['adjusted_file_path']):
                continue
            self.download_file(val)
            self.modify_pdf(val)
        self.browser.close_all_tabs_except_primary()

    def download_file(self, value):
        self.browser.wait_click(By.XPATH, f"//tr[td[normalize-space(text())='{value['title']}']]")
        self.browser.driver.execute_script("ConsumersList();")
        self.browser.wait_for_page_load()
        self.browser.send_keys(By.NAME, "toDate", value['import_date'])
        self.browser.driver.execute_script("ExportReadings();")
        self.browser.wait_for_file_count_increase(60)
        time.sleep(.25)
        os.rename(value['file_path'], value['adjusted_file_path'])
        self.browser.switch_to_primary_tab()
        self.browser.driver.execute_script("SitesList();")

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