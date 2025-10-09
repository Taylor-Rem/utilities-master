from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import kmc_url
from datetime import datetime
import time

class ResmapImport:
    def __init__(self, browser, thread):
        self.browser = browser
        self.thread = thread

    def import_file(self, propid, dropdown_values, file_path, import_date):
        self.browser.driver.get(f"{kmc_url}properties/{propid}/imports")
        time.sleep(1)
        self.browser.driver.refresh()
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
                return
            self.browser.wait_click(By.XPATH, dropdown['value'])
            self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'ul.popup')
            self.browser.wait_click(By.XPATH, dropdown['key'])

        if self.thread.is_cancelled:
            return
        
        # Wait for the date input element
        date_input = self.browser.wait_for_presence_of_element(
            By.CSS_SELECTOR, 'details.date_picker summary.input_wrapper input'
        )

        # Convert date to YYYY-MM-DD
        formatted_date = datetime.strptime(import_date, '%m/%d/%Y').strftime('%Y-MM-DD')

        # Use the Vue component's setDate method to actually set the date
        self.browser.driver.execute_script("""
            const input = arguments[0];
            const date = arguments[1];
            // Find the closest date_picker component
            const details = input.closest('details.date_picker');
            const vueComponent = details.__vue__;
            if (vueComponent) {
                if (vueComponent.type === 'month') {
                    vueComponent.setMonth(date);
                } else {
                    const day = parseInt(date.split('-')[2]);
                    vueComponent.setDate(day);
                }
            }
        """, date_input, formatted_date)

        if self.thread.is_cancelled:
            return

        self.browser.wait_for_presence_of_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(file_path)
        self.browser.wait_for_load()
        if self.thread.is_cancelled:
            return
        time.sleep(3)
        self.browser.wait_click(By.XPATH, '//div[contains(@class, "flex-row alert-info full-width")]/button[@type="button" and contains(@class, "primary push_button")]')
        self.browser.wait_for_load()