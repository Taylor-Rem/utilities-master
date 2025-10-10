from config import beacon_username, beacon_password
from selenium.webdriver.common.by import By
from job_manager.jobs.jobs_base import JobsBase
from resmap_ops.resmap_import import ResmapImport
import os, time

class Beacon(JobsBase):
    def __init__(self, browser, job_info, thread):
        super().__init__(browser, job_info, thread)
        # self.resmap_import = ResmapImport(browser, thread)
        self.run_job()

    def run_job(self):
        self.browser.driver.get(self.job_info['beacon_url'])
        self.browser.wait_send_keys(By.ID, "username", beacon_username, "enter")
        self.browser.wait_send_keys(By.ID, "formField:Rkrir55:", beacon_password, "enter")
        self.browser.wait_click(By.ID, "nav_link_header_monitor")
        self.browser.wait_click(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[3]/div[5]")
        time.sleep(.25)
        self.browser.wait_click(By.XPATH, "//div[@class='facet-terms']//p[@class='see-more']")

        for value in self.job_info['info']:
            if not value['include']:
                continue
            self.browser.wait_click(By.ID, f"route_{value['park_num']}_{value['short_name']}")
            self.browser.wait_scroll_click(By.ID, 'batch-actions')
            self.browser.wait_click(By.ID, 'action-export-data')
            self.browser.wait_click(By.ID, 'export_billing_reads')
            self.browser.wait_send_keys(By.ID, 'data-export-billingreads-datepicker', value['import_date'], "tab")
            self.browser.wait_click(By.ID, 's2id_tolerance')
            self.browser.wait_click(By.XPATH, '//*[@id="select2-drop"]/ul/li[5]/div')
            self.browser.wait_click(By.ID, 'btn-export-new')
            self.browser.wait_click(By.ID, 'export_result_url', timeout=200)
            print('hello')