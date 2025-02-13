from PyQt5.QtWidgets import QLabel, QVBoxLayout
from front_end.base_windows.methods import Methods

class Thread(Methods):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.thread_controller = None  # will hold our QThread instance
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Running Operation')
        # Create a label to show progress messages.
        self.progress_label = QLabel("Starting...", self)
        self.layout.addWidget(self.progress_label)
        # Create a Cancel button.
        self.create_button('Cancel', self.cancel_operation)

    def update_progress(self, message):
        # Slot to update progress from the thread.
        self.progress_label.setText(message)

    def on_finished(self):
        # Called when the thread signals completion.
        self.progress_label.setText("Operation finished!")
        # Optionally, switch back to the main window after a delay or immediately.
        self.controller.switch_window('main')

    def on_error(self, error_message):
        # Called if the thread signals an error.
        self.progress_label.setText(f"Error: {error_message}")

    def cancel_operation(self):
        # Called when the user clicks Cancel.
        if self.thread_controller:
            self.thread_controller.cancel()
            self.update_progress("Cancellation requested...")
            self.controller.switch_window('main')