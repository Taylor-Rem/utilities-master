from config import beacon_username, beacon_password
from selenium.webdriver.common.by import By
from job_manager.jobs.jobs_base import JobsBase
from resmap_ops.resmap_import import ResmapImport
from file_manager.csv_manager import CsvManager
import pandas as pd
import os, time


class Beacon(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        self.resmap_import = ResmapImport(browser, thread)
        self.run_job()

    def run_job(self):
        self.remove_source_file()
        if any(not os.path.exists(value['adjusted_file_path']) for value in self.job_info['info']):
            self.download_from_beacon()
        self.split_csv_by_prop()
        self.remove_source_file()
        self.import_to_resmap()

    def download_from_beacon(self):
        self.browser.driver.get(self.job_info['beacon_url'])
        self.login()

        # Navigate and expand filters
        self.browser.wait_click(By.ID, "nav_link_header_monitor")
        self.browser.wait_click(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[3]/div[5]")
        self.browser.wait_scroll_click(By.XPATH, "//div[@class='facet-terms']//p[@class='see-more']")

        for value in self.job_info['info']:
            if not os.path.exists(value['adjusted_file_path']):
                self.browser.wait_scroll_click(By.ID, f"route_{value['park_num']}_{value['short_name']}")

        self.download_file_from_beacon(self.job_info['info'][0]['import_date_obj'])

    def download_file_from_beacon(self, import_date):
        self.browser.wait_scroll_click(By.ID, 'batch-actions')
        self.browser.wait_click(By.ID, 'action-export-data')
        self.browser.wait_click(By.ID, 'export_billing_reads')
        self.browser.wait_send_keys(By.ID, 'data-export-billingreads-datepicker', import_date.toString('MM/dd/yyyy'), "tab")
        self.browser.wait_click(By.ID, 's2id_tolerance')
        self.browser.wait_click(By.XPATH, '//*[@id="select2-drop"]/ul/li[7]/div')
        self.browser.wait_click(By.ID, 'btn-export-new')
        self.browser.wait_click(By.ID, 'export_result_url', timeout=500)
        time.sleep(0.25)
        self.browser.wait_for_downloads_to_finish()
        self.browser.wait_click(By.CSS_SELECTOR, 'a.simplemodal-close.close')

    def split_csv_by_prop(self):
        source_csv = pd.read_csv(self.job_info['info'][0]['file_path'])
        
        # Safely extract prefix, converting non-numeric values to NaN
        source_csv['prefix'] = pd.to_numeric(
            source_csv['Account_ID'].astype(str).str.split('_', n=1).str[0],
            errors='coerce'
        )
        
        # Filter out rows where prefix could not be converted to a number (e.g., 'UNKNOWN')
        source_csv = source_csv[source_csv['prefix'].notna()]
        
        # Ensure prefix is integer type after filtering
        source_csv['prefix'] = source_csv['prefix'].astype(int)
        
        for val in self.job_info['info']:
            source_csv[source_csv['prefix'] == val['entity_code']].to_csv(
                val['adjusted_file_path'], index=False
            )

    def import_to_resmap(self):
        for value in self.job_info['info']:
            if self.cancelled():
                return
            self.resmap_import.import_file(
                value['propid'], value['dropdowns'], value['adjusted_file_path'], value['import_date']
            )

    def remove_source_file(self):
        try:
            os.remove(self.job_info['info'][0]['file_path'])
        except FileNotFoundError:
            pass

    def login(self):
        self.browser.wait_send_keys(By.ID, "username", beacon_username, "enter")
        self.browser.wait_send_keys(By.ID, "formField:Rkrir55:", beacon_password, "enter")
