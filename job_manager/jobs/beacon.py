from config import beacon_username, beacon_password
from selenium.webdriver.common.by import By
from job_manager.jobs.jobs_base import JobsBase
from resmap_ops.resmap_import import ResmapImport
from file_manager.csv_manager import CsvManager
import os, time

class Beacon(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        self.resmap_import = ResmapImport(browser, thread)
        self.run_job()

    def run_job(self):
        self.os_operations()
        if any(not os.path.exists(value['adjusted_file_path']) for value in self.job_info['info']):
            self.download_from_beacon()
        self.import_to_resmap()

    def download_from_beacon(self):
        self.browser.driver.get(self.job_info['beacon_url'])
        self.login()
        self.browser.wait_click(By.ID, "nav_link_header_monitor")
        self.browser.wait_click(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[3]/div[5]")

        for value in self.job_info['info']:
            if not value['include']:
                continue
            if not os.path.exists(value['adjusted_file_path']):
                self.download_file_from_beacon(value)

    def download_file_from_beacon(self, value):
        time.sleep(.5)
        self.browser.wait_scroll_click(By.XPATH, "//div[@class='facet-terms']//p[@class='see-more']")
        self.browser.wait_scroll_click(By.ID, f"route_{value['park_num']}_{value['short_name']}")
        time.sleep(.5)
        self.browser.scroll_to_top()
        time.sleep(.5)
        self.browser.wait_click(By.ID, 'batch-actions')
        self.browser.wait_click(By.ID, 'action-export-data')
        self.browser.wait_click(By.ID, 'export_billing_reads')
        self.browser.wait_send_keys(By.ID, 'data-export-billingreads-datepicker', value['import_date'], "tab")
        self.browser.wait_click(By.ID, 's2id_tolerance')
        self.browser.wait_click(By.XPATH, '//*[@id="select2-drop"]/ul/li[7]/div')
        self.browser.wait_click(By.ID, 'btn-export-new')
        self.browser.wait_click(By.ID, 'export_result_url', timeout=200)
        time.sleep(.25)
        self.browser.wait_for_downloads_to_finish()
        self.modify_downloaded_file(value)
        self.browser.wait_click(By.CSS_SELECTOR, 'a.simplemodal-close.close')
        self.browser.wait_click(By.XPATH, "//div[@class='close']")


    def import_to_resmap(self):
        for value in self.job_info['info']:
            if not value['include']:
                continue
            if self.cancelled():
                return
            self.resmap_import.import_file(value['propid'], value['dropdowns'], value['adjusted_file_path'], value['import_date'])

    def os_operations(self):
        try:
            os.remove(self.job_info['info'][0]['file_path'])
        except FileNotFoundError:
            pass
        for value in self.job_info['info']: value['adjusted_file_path'] = f"{value['adjusted_file_path']}-{value['import_date'].replace('/', '-')}.csv"

    def modify_downloaded_file(self, value):
        os.rename(value['file_path'], f"{value['adjusted_file_path']}")
        # csv_manager = CsvManager(value['adjusted_file_path'])
        # csv_manager.convert_units()
        # csv_manager.delete_empty_rows()
        # csv_manager.save_csv()

    def login(self):
        self.browser.wait_send_keys(By.ID, "username", beacon_username, "enter")
        self.browser.wait_send_keys(By.ID, "formField:Rkrir55:", beacon_password, "enter")