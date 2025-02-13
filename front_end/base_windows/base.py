from PyQt5.QtWidgets import QWidget, QVBoxLayout

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

