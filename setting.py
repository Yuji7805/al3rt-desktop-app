from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                             QPushButton, QApplication)


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.model_selection_label = QLabel("NLP Model Selection")
        layout.addWidget(self.model_selection_label)

        self.model_selection_combo = QComboBox(self)
        self.model_selection_combo.addItems(['Model 1', 'Model 2'])
        layout.addWidget(self.model_selection_combo)

        self.manage_streams_button = QPushButton("Manage Streams", self)
        layout.addWidget(self.manage_streams_button)

        self.manage_prompts_button = QPushButton("Manage Prompts", self)
        layout.addWidget(self.manage_prompts_button)

        # Set Layout and Window Title
        self.setLayout(layout)
        self.setWindowTitle('Settings Window')

        # Connect Button Clicks
        self.manage_streams_button.clicked.connect(self.manage_streams)
        self.manage_prompts_button.clicked.connect(self.manage_prompts)

    def manage_streams(self):
        print("Manage Streams Clicked")

    def manage_prompts(self):
        print("Manage Prompts Clicked")

    def closeEvent(self, event):
        self.hide()
        event.ignore()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    setting_win = SettingWindow()
    setting_win.show()
    sys.exit(app.exec_())
