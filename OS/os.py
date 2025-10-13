import os, glob
from datetime import datetime
from config import pc_username, download_path

class Os:
    def __init__(self):
        self.year = datetime.now().strftime("%Y")
        self.month = datetime.now().strftime("%m")
        self.day = datetime.now().strftime("%d")
        self.today_date = f"{self.month}/{self.day}/{self.year}"
        self.today_date_file = f"{self.month}-{self.day}-{self.year}"

    def adjust_file_path(self, title, date=None):
        if not date:
            date = self.today_date
        date_info = date.split("/")
        return os.path.join(download_path, f"SPUD for KMC {title} {date_info[0]}_{date_info[1]}_{date_info[2]}.csv")

    def rename_file(self, new_name):
        new_path = os.path.join(os.path.dirname(self.file_path), new_name)
        os.rename(self.file_path, new_path)
        self.file_path = new_path

    def replace_file_path(self, old_path, new_path):
        os.rename(old_path, new_path)