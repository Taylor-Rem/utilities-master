import os
from datetime import datetime
from config import pc_username

class Os:
    def __init__(self, job):
        self.year = datetime.now().strftime("%Y")
        self.month = datetime.now().strftime("%m")
        self.day = datetime.now().strftime("%d")
        self.today_date = f"{self.month}/{self.day}/{self.year}"
        self.init(job)

    def init(self, job):
        match job:
            case "abt":
                self.download_dir = f"/Users/{pc_username}/Downloads/bot_downloads"

    def adjust_file_path(self, title, date):
        date_info = date.split("/")
        return os.path.join(self.download_dir, f"SPUD for KMC {title} {date_info[0]}_{date_info[1]}_{date_info[2]}.csv")
