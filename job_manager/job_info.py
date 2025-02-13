from OS.os import Os
from config import kmc_username, kmc_password

class JobInfo:
    def __init__(self, job):
        # Local Host
        self.kmc_url_start = 'http://localhost:8080/#/'
        # Live
        # self.kmc_url_start = 'https://residentmap.kmcmh.com/#/'
        self.init(job)

    def init(self, job):
        os_ops = Os()
        self.job_info = {}
        self.return_info = {}
        self.job_info['title'] = job
        self.job_info['login_info']= {'kmc_username': kmc_username, 'kmc_password': kmc_password}
        match job:
            case 'abt':
                self.job_info['info'] = self.abt_import(os_ops)
            case 'cereniti':
                self.job_info['info'] = self.cereniti_import()

    def abt_import(self, os_ops):
        abt_url_start = 'http://12.175.8.66/Usage%20Reports/All/KMC%20'

        property_info = [
            {"title": "Arapaho Village", "propid": 76, 'abt_url': 'Arapaho%20Village.html', 'day': 15},
            {"title": "Haven Cove", "propid": 66, 'abt_url': 'Haven%20Cove.html', 'day': 10},
            {"title": "Lake Villa", "propid": 59, 'abt_url': 'Lake%20Villa.html', 'day': 10}
            ]
        
        for value in property_info:
            import_date = f"{os_ops.month}/{value['day']}/{os_ops.year}"
            self.return_info[value['title']] = {
                'abt_url': f"{abt_url_start}{value['abt_url']}",
                'kmc_url': f'{self.kmc_url_start}properties/{value['propid']}/imports',
                'import_date': import_date,
                'file_path': os_ops.adjust_file_path(value['title'], import_date, self.job_info['title']),
                'dropdowns': ["Utility Reads - ABT", "Water"]
            }
        return self.return_info

    def cereniti_import(self):
        property_info = [
            {"title": "Sherwood Forest", "propid": 3, "cereniti_url": 'blah'},
            {"title": "Westcrest Water", "propid": 18, "cereniti_url": 'blah'},
            {"title": "Westcrest Electric", "propid": 18, "cereniti_url": 'blah'},
            {"title": "Shadow Ridge", "propid": 37, "cereniti_url": 'blah'},
            {"title": "Majestic Oaks", "propid": 13, "cereniti_url": 'blah'},
            {"title": "Mountain View", "propid": 14, "cereniti_url": 'blah'}
        ]

        for value in property_info:
            self.return_info[value['title']] = {
                'cereniti_url': 'blah',
                'kmc_url': f'{self.kmc_url_start}properties/{value['propid']}/imports',
            }