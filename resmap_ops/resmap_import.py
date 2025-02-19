from selenium.webdriver.common.by import By
from config import kmc_url

class ResmapImport:
    def __init__(self, browser, thread):
        self.browser = browser
        self.thread = thread

    def import_file(self, propid, dropdown_values, file_path):
        self.browser.driver.get(f"{kmc_url}/properties/{propid}/imports")
        self.browser.wait_login()
        dropdowns = [{
                'value': '//div[@class="flex-row card-text"]//details[@class="auto_complete"]',
                'key': f'//li[normalize-space(text())="{dropdown_values[0]}"]'
            },{
                'value': '//div[@class="alert-info full-width"]//details[@class="auto_complete"]', 
                'key': f'//li[normalize-space(text())="{dropdown_values[1]}"]'
            }]
        for dropdown in dropdowns:
            if self.thread.is_cancelled:
                break
            self.browser.wait_click(By.XPATH, dropdown['value'])
            self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'ul.popup')
            self.browser.wait_click(By.XPATH, dropdown['key'])

        if self.thread.is_cancelled:
            return
        self.browser.wait_for_downloads()
        self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(file_path)
        self.browser.wait_for_load()
        if self.thread.is_cancelled:
            return
        self.browser.wait_click(By.XPATH, '//div[contains(@class, "flex-row alert-info full-width")]/button[@type="button" and contains(@class, "primary push_button")]')
        self.browser.wait_for_load()