from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    ElementNotInteractableException,
)

from config import pc_username
import time
import os

class BrowserBase:
    def __init__(self):
        options = Options()
        self.download_dir = f"/Users/{pc_username}/Downloads/bot_downloads"
        options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,  # Set the download directory
            "download.prompt_for_download": False,       # Disable download prompts
            "download.directory_upgrade": True,          # Automatically overwrite
            "safebrowsing.enabled": True                 # Enable safe browsing
        })
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

class BrowserMethods(BrowserBase):
    def __init__(self):
        super().__init__()

        import time

    def wait_for_downloads(self, timeout=30):
        """Wait for all downloads to complete in the given directory."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            # Check if there are any incomplete downloads
            files = os.listdir(self.download_dir)
            if not any(file.endswith('.crdownload') or file.endswith('.part') for file in files):
                return True
            time.sleep(1)  # Wait a bit before re-checking
        raise TimeoutError("Download did not complete within the timeout period.")
    
    def wait_for_page_load(self):
        self.wait_for_presence_of_element(By.TAG_NAME, "body")    

    def wait_for_presence_of_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_for_load(self):
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loading_spinner")))

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except Exception as e:
            print(f"Error finding element {e}")
            return None

    def find_click(self, by, value):
        element = self.find_element(by, value)
        element.click()

    def send_keys(self, by, value, keys, enter=False):
        element = self.find_element(by, value)
        if element:
            self.send_keys_to_element(element, keys, enter)

    def send_keys_to_element(self, element, keys, enter=False):
        try:
            element.clear()
            element.send_keys(keys)
            if enter:
                element.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            print("Error: Element is not interactable.")

    def find_select(self, by, value, selectValue):
        element = self.find_element(by, value)
        Select(element).select_by_visible_text(selectValue)
    
    def wait_click(self, by, value):
        element = self.wait_for_presence_of_element(by, value)
        element.click()

    def login(self, username, password):
        try:
            self.send_keys(By.NAME, "username", username)
            self.send_keys(By.NAME, "password", password, True)
        except NoSuchElementException:
            pass

    def wait_login(self, username, password):
        self.wait_for_page_load()
        self.login(username, password)

class Browser(BrowserMethods):
    def __init__(self):
        super(Browser, self).__init__()
    