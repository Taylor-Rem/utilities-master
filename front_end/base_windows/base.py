from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 400)
        self.setMinimumSize(250, 600)
        
        # Create a widget to hold the layout
        self.content_widget = QWidget()
        self.layout = QVBoxLayout(self.content_widget)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.content_widget)
        
        # Set main layout for the window
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)