from front_end.base_windows.methods import Methods
from functools import partial

class JobMethods(Methods):
    def __init__(self):
        super().__init__()

    def set_job_info(self, job_info):
        for info in job_info['info']:
            self.include_properties(info['title'], info)
            self.create_dates(info)
            
    def include_properties(self, title, info):
        info['include'] = True
        checkbox = self.create_checkbox(title)
        checkbox.stateChanged.connect(
            lambda state, cb=checkbox, inf=info: inf.update({'include': cb.isChecked()})
        )

    def create_dates(self, info):
        date_input = self.create_date_input(info['import_date'])
        info['import_date_obj'] = date_input.date()
        date_input.dateChanged.connect(
            lambda date, inf=info: inf.update({'import_date': date.toString("yyyy-MM-dd"), 'import_date_obj': date}))