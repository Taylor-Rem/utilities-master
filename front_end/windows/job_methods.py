from front_end.base_windows.methods import Methods
from functools import partial

class JobMethods(Methods):
    def __init__(self):
        super().__init__()

    def abt_info(self, job_info):
        for title, info in job_info['info'].items():
            self.include_properties(title, info)
            date_input = self.create_text_input(info['import_date'], info['import_date'])
            date_input.textChanged.connect(
                lambda text, tit=title, inf=info: self.handle_date_change(text, tit, inf, job_info['title']))
            
    def cereniti_info(self, job_info):
        for title, info in job_info['info'].items():
            self.include_properties(title, info)
            
    def include_properties(self, title, info):
        info['include'] = True
        checkbox = self.create_checkbox(title)
        checkbox.stateChanged.connect(
            lambda state, cb=checkbox, inf=info: inf.update({'include': cb.isChecked()})
        )