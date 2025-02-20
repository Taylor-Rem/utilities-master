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

    def adjust_file_path(self, title, job_name, date=None):
        if not date:
            date = self.today_date
        date_info = date.split("/")
        match job_name:
            case 'abt':
                return os.path.join(download_path, f"SPUD for KMC {title} {date_info[0]}_{date_info[1]}_{date_info[2]}.csv")
