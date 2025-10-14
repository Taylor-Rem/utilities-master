from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    ElementNotInteractableException,
)

from config import download_path, kmc_username, kmc_password
import time
import os

class BrowserBase:
    def __init__(self):
        self.timeout_time = 60
        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": download_path,  # Set the download directory
            "download.prompt_for_download": False,       # Disable download prompts
            "download.directory_upgrade": True,          # Automatically overwrite
            "safebrowsing.enabled": True                 # Enable safe browsing
        })
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.wait = WebDriverWait(self.driver, self.timeout_time)
        self.primary_tab = None

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

class BrowserMethods(BrowserBase):
    def __init__(self):
        super().__init__()

    def new_tab(self):
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_primary_tab(self):
        if self.primary_tab is None:
            self.primary_tab = self.driver.window_handles[0]
        else:
            try:
                current_tab = self.driver.current_window_handle
                if current_tab != self.primary_tab:
                    self.driver.close()
            except NoSuchWindowException:
                pass
        self.driver.switch_to.window(self.primary_tab)

    def close_all_tabs_except_primary(self):
        if self.primary_tab is None:
            self.primary_tab = self.driver.window_handles[0]
        try:
            # Get all current window handles
            all_tabs = self.driver.window_handles
            
            # Loop through all tabs except the primary tab
            for tab in all_tabs:
                if tab != self.primary_tab:
                    # Switch to the tab
                    self.driver.switch_to.window(tab)
                    # Close it
                    self.driver.close()
        
            # Switch back to primary tab
            self.driver.switch_to.window(self.primary_tab)
        except NoSuchWindowException:
            pass

    def wait_for_file_count_increase(self, timeout=30):
        """Wait for the number of files in the download directory to increase."""
        initial_file_count = len(os.listdir(download_path))
        end_time = time.time() + timeout

        while time.time() < end_time:
            current_file_count = len(os.listdir(download_path))
            if current_file_count > initial_file_count:
                return True  # A new file has appeared in the directory
            
            time.sleep(0.5)  # Check again after a short delay
        
        raise TimeoutError("Download did not start within the timeout period.")


    def wait_for_download_to_start(self, timeout=30):
        """Wait for a download to start in the given directory."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            files = os.listdir(download_path)
            if any(file.endswith('.crdownload') or file.endswith('.part') for file in files):
                return True  # A download has started
            time.sleep(0.5)  # Check again after a short delay
        raise TimeoutError("Download did not start within the timeout period.")


    def wait_for_downloads_to_finish(self, timeout=30):
        """Wait for all downloads to complete in the given directory."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            # Check if there are any incomplete downloads
            files = os.listdir(download_path)
            if not any(file.endswith('.crdownload') or file.endswith('.part') for file in files):
                return True
            time.sleep(.5)  # Wait a bit before re-checking
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

    def wait_send_keys(self, by, value, keys, extra=None):
        element = self.wait_for_presence_of_element(by, value)
        if element:
            self.send_keys_to_element(element, keys, extra)

    def send_keys(self, by, value, keys, extra=None):
        element = self.find_element(by, value)
        if element:
            self.send_keys_to_element(element, keys, extra)

    def wait_scroll_click(self, by, value):
        element = self.wait_for_element_clickable(by, value)
        self.scroll_to_element(element)
        time.sleep(1)
        element.click()

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # actions = ActionChains(self.driver)
        # actions.move_to_element(element).perform()

    def send_keys_to_element(self, element, keys, extra=None):
        try:
            element.clear()
            element.send_keys(keys)
            if extra:
                element.send_keys(getattr(Keys, extra.upper()))
        except ElementNotInteractableException:
            print("Error: Element is not interactable.")

    def find_select(self, by, value, selectValue):
        element = self.find_element(by, value)
        Select(element).select_by_visible_text(selectValue)

    def wait_for_element_clickable(self, by, value, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_click(self, by, value, timeout=None):
        element = self.wait_for_element_clickable(by, value, timeout)
        element.click()

    def login(self, username=kmc_username, password=kmc_password):
        try:
            self.send_keys(By.NAME, "username", username)
            self.send_keys(By.NAME, "password", password, "enter")
        except NoSuchElementException:
            pass

    def wait_login(self, username=kmc_username, password=kmc_password):
        self.wait_for_page_load()
        self.login(username, password)

    def define_rows(self, by, value):
        tbody = self.wait_for_presence_of_element(by, value)
        return tbody.find_elements(By.XPATH, ".//tr")

class Browser(BrowserMethods):
    def __init__(self):
        super(Browser, self).__init__()
    