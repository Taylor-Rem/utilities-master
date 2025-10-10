from front_end.base_windows.methods import Methods
from functools import partial

class JobMethods(Methods):
    def __init__(self):
        super().__init__()

    def set_job_info(self, job_info):
        for info in job_info['info']:
            self.include_properties(info['title'], info)
            self.change_dates(info, job_info['title'])

    # def abt_info(self, job_info):
    #     for info in job_info['info']:
    #         self.include_properties(info['title'], info)
    #         self.change_dates(info, job_info['title'])
            
    # def cereniti_info(self, job_info):
    #     for info in job_info['info']:
    #         self.include_properties(info['title'], info)
    #         self.change_dates(info, job_info['title'])
            
    def include_properties(self, title, info):
        info['include'] = True
        checkbox = self.create_checkbox(title)
        checkbox.stateChanged.connect(
            lambda state, cb=checkbox, inf=info: inf.update({'include': cb.isChecked()})
        )

    def change_dates(self, info, job_title):
        date_input = self.create_text_input(info['import_date'], info['import_date'])
        date_input.textChanged.connect(
            lambda text, tit=info['title'], inf=info: self.handle_date_change(text, tit, inf, job_title))