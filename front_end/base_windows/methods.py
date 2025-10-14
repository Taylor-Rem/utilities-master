from front_end.base_windows.base import BaseWindow
from OS.os import Os
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QPushButton


class Methods(BaseWindow):
    def __init__(self):
        super().__init__()

    def create_button(self, title, function):
        button = QPushButton(title, self)
        button.clicked.connect(function)
        self.layout.addWidget(button)

    def create_checkbox(self, title, initial_state=True):
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
    
    def create_date_input(self, date_str):
        date_input = NoScrollDateEdit(self)
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        date_input.setDate(date)
        date_input.setCalendarPopup(True)
        self.layout.addWidget(date_input)
        return date_input

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

class NoScrollDateEdit(QDateEdit):
    def wheelEvent(self, event):
        event.ignore()              