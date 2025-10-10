from OS.os import Os
from config import download_path, beacon_park_info_path
from job_manager.property_info import property_info_obj
import pandas as pd
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
            case 'beacon':
                self.job_info['beacon_url'] = "https://beaconama.net/admin/portfolio/at_a_glance"
                self.job_info['info'] = self.beacon_import()

    def abt_import(self):
        abt_url_start = 'http://12.175.8.66/Usage%20Reports/All/KMC%20'
        property_info = self.get_property_info(["Arapaho Village", "Haven Cove", "Lake Villa"])

        return [
            {
                'title': value['title'],
                'abt_url': f"{abt_url_start}{value['abt_url']}",
                'propid': value['propid'],
                'import_date': f"{self.os_ops.month}/{value['day']}/{self.os_ops.year}",
                'file_path': self.os_ops.adjust_file_path(value['title'], f"{self.os_ops.month}/{value['day']}/{self.os_ops.year}"),
                'dropdowns': ["Utility Reads - ABT", "Water"]
            }
            for value in property_info
        ]

    def cereniti_import(self):
        property_info = self.get_property_info([
            "Sherwood Forest", "Westcrest", "Shadow Ridge", "Majestic Oaks", "Mountain View", "Westcrest Electric"
        ])

        return [
            {
                'title': value['title'],
                'propid': value['propid'],
                'import_date': f"{self.os_ops.month}/{value['day']}/{self.os_ops.year}",
                'file_path': f"{download_path}/{re.sub(r'[\s-]+', '_', value['title'].strip().lower())}.csv",
                'adjusted_file_path': f"{download_path}/{re.sub(r'[\s-]+', '_', value['title'].strip().lower())}-{self.os_ops.month}-{value['day']}-{self.os_ops.year}.csv",
                'dropdowns': ["Utility Reads - Cereniti", "Water" if 'fee' not in value else value['fee']],
            }
            for value in property_info
        ]
    
    def beacon_import(self):
        df = pd.read_csv(beacon_park_info_path)
        not_uploaded = df[df['uploaded'].astype(str).str.upper() == 'FALSE']

        return [
            {
                'title': row['full_name'],
                'propid': row['propid'],
                'import_date': f"{self.os_ops.month}/{row['beacon_import_date']}/{self.os_ops.year}",
                'park_num': row['park_num'],
                'short_name': row['shortened_name']
            }
            for _, row in not_uploaded.iterrows()
        ]

    def get_property_info(self, properties):
        return [property_info_obj[p] for p in properties]