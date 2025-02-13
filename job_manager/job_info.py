from OS.os import Os
from config import pc_username, kmc_username, kmc_password

class JobInfo:
    def __init__(self, job):
        # Local Host
        self.kmc_url_start = 'http://localhost:8080/#/'
        # Live
        # self.kmc_url_start = 'https://residentmap.kmcmh.com/#/'
        self.init(job)

    def init(self, job):
        os_ops = Os(job)
        self.job_info = {}
        self.job_info['title'] = job
        self.job_info['login_info']= {'kmc_username': kmc_username, 'kmc_password': kmc_password}
        match job:
            case 'abt':
                self.job_info['info'] = self.abt_import(os_ops)

    def abt_import(self, os_ops):
        return_info = {}
        abt_url_start = 'http://12.175.8.66/Usage%20Reports/All/KMC%20'

        property_info = [
            {"title": "Arapaho Village", "propid": 76, 'abt_url': 'Arapaho%20Village.html', 'day': 15},
            {"title": "Haven Cove", "propid": 66, 'abt_url': 'Haven%20Cove.html', 'day': 10},
            {"title": "Lake Villa", "propid": 59, 'abt_url': 'Lake%20Villa.html', 'day': 10}
            ]
        
        for value in property_info:
            import_date = f"{os_ops.month}/{value['day']}/{os_ops.year}"
            return_info[value['title']] = {
                'abt_url': f"{abt_url_start}{value['abt_url']}",
                'kmc_url': f'{self.kmc_url_start}properties/{value['propid']}/imports',
                'import_date': import_date,
                'file_path': os_ops.adjust_file_path(value['title'], import_date)
            }
        return return_info
