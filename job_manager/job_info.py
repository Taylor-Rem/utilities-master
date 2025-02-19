from OS.os import Os
from config import download_path
import re

class JobInfo:
    def __init__(self, job):
        self.job_info = {}
        self.job_info['title'] = job
        self.init()

    def init(self):
        self.os_ops = Os()
        match self.job_info['title']:
            case 'abt':
                self.job_info['info'] = self.abt_import()
            case 'cereniti':
                self.job_info['cereniti_url'] = "https://www.myspeednet.net"
                self.job_info['info'] = self.cereniti_import()

    def abt_import(self):
        return_info = {}
        abt_url_start = 'http://12.175.8.66/Usage%20Reports/All/KMC%20'
        property_info = [
            {"title": "Arapaho Village", "propid": 76, 'abt_url': 'Arapaho%20Village.html', 'day': 15},
            {"title": "Haven Cove", "propid": 66, 'abt_url': 'Haven%20Cove.html', 'day': 10},
            {"title": "Lake Villa", "propid": 59, 'abt_url': 'Lake%20Villa.html', 'day': 10}
            ]
        for value in property_info:
            import_date = f"{self.os_ops.month}/{value['day']}/{self.os_ops.year}"
            return_info[value['title']] = {
                'abt_url': f"{abt_url_start}{value['abt_url']}",
                'propid': value['propid'],
                'import_date': import_date,
                'file_path': self.os_ops.adjust_file_path(value['title'], self.job_info['title'], import_date),
                'dropdowns': ["Utility Reads - ABT", "Water"]
            }
        return return_info

    def cereniti_import(self):
        return_info = {}
        property_info = [
            {"title": "Sherwood Forest", "propid": 3, "target_id": 846},
            {"title": "Westcrest", "propid": 18, "target_id": 847},
            {"title": "Westcrest Electric", "propid": 18, "fee": "Electric", "target_id": 848},
            {"title": "Shadow Ridge", "propid": 37, "target_id": 849},
            {"title": "Majestic Oaks", "propid": 13, "target_id": 850},
            {"title": "Mountain View", "propid": 14, "target_id": 868}
        ]
        for value in property_info:
            file_path = f"{download_path}/{re.sub(r'[\s-]+', '_', value['title'].strip().lower())}"
            return_info[value['title']] = {
                'propid': value['propid'],
                'file_path': f"{file_path}.csv",
                'adjusted_file_path': f"{file_path}-{self.os_ops.today_date}.csv",
                'dropdowns': ["Utility Reads - Cereniti", "Water" if 'fee' not in value else value['fee']]
            }
        return return_info