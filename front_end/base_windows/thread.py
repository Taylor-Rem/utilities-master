from PyQt5.QtWidgets import QLabel, QVBoxLayout
from front_end.base_windows.methods import Methods

class Thread(Methods):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.thread_controller = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Active Operation')

        self.layout.addWidget(QLabel("Running Operation"))

        self.create_button('Cancel', self.cancel_operation)

    def cancel_operation(self):
        if self.thread_controller:
            self.thread_controller.cancel()
            self.finish_operation()

    def finish_operation(self):
        self.controller.switch_window('main')