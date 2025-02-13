from front_end.base_windows.base import BaseWindow
from OS.os import Os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QPushButton


class Methods(BaseWindow):
    def __init__(self):
        super().__init__()

    def create_button(self, title, function):
        button = QPushButton(title, self)
        button.clicked.connect(function)
        self.layout.addWidget(button)

    def create_checkbox(self, title, initial_state=False):
        checkbox = QCheckBox(title, self)
        checkbox.setChecked(initial_state)
        self.layout.addWidget(checkbox)
        return checkbox
    
    def create_text_input(self, placeholder="", initial=""):
        text_input = QLineEdit(self)
        text_input.setPlaceholderText(placeholder)
        text_input.setText(initial)
        self.layout.addWidget(text_input)
        return text_input
    
    def handle_date_change(self, text, tit, inf, job_title):
        inf.update({'import_date': text})
        inf.update({'file_path': Os(job_title).adjust_file_path(tit, text)})

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()