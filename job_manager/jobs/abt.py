from selenium.webdriver.common.by import By
import os

class Abt:
    def __init__(self, browser, job_info, thread):
        self.browser = browser
        self.thread = thread
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
            self.upload_to_manage_portal(value)

    def download_from_abt(self, property):
        self.browser.driver.get(property['abt_url'])
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Export a Readings File"]')
        self.browser.send_keys(By.XPATH, '//input[@type="TEXT" and @name="The Date"]', property['import_date'])
        self.browser.find_select(By.NAME, 'ExportFormat', 'Starnik')
        if self.thread.is_cancelled:
            return
        self.browser.find_click(By.XPATH, '//input[@type="submit" and @value="Go!"]')

    def upload_to_manage_portal(self, property):
        self.browser.driver.get(property['kmc_url'])
        self.browser.wait_login(self.login_info['kmc_username'], self.login_info['kmc_password'])
        self.select_kmc_element(property)


    def select_kmc_element(self, property):
        dropdowns = [
            {'value': '//div[@class="flex-row card-text"]//details[@class="auto_complete"]', 'key': '//li[normalize-space(text())="Utility Reads - ABT"]'},
            {'value': '//div[@class="alert-info full-width"]//details[@class="auto_complete"]', 'key': '//li[normalize-space(text())="Water"]'}
            ]
        for dropdown in dropdowns:
            if self.thread.is_cancelled:
                break
            self.browser.wait_click(By.XPATH, dropdown['value'])
            self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'ul.popup')
            self.browser.wait_click(By.XPATH, dropdown['key'])

        if self.thread.is_cancelled:
            return
        self.browser.wait_for_downloads()
        self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(property['file_path'])
        self.browser.wait_for_load()
        if self.thread.is_cancelled:
            return
        self.browser.wait_click(By.XPATH, '//div[contains(@class, "flex-row alert-info full-width")]/button[@type="button" and contains(@class, "primary push_button")]')
        self.browser.wait_for_load()
