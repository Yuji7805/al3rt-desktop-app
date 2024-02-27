from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QTextEdit, QComboBox, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase
from setting import SettingWindow


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_window = SettingWindow()

        self.initUI()
        self.load_prompts()
        self.load_streams()

        # Connect the signal to the slot
        self.setting_window.prompts_updated.connect(self.load_prompts)

    def initUI(self):
        vlayout = QVBoxLayout()
        hselectlayout = QHBoxLayout()

        self.stream_combo = QComboBox()
        hselectlayout.addWidget(self.stream_combo)

        self.prompt_select_combo = QComboBox()
        hselectlayout.addWidget(self.prompt_select_combo)

        self.setting_button = QPushButton("Setting")
        self.setting_button.setFixedWidth(22)
        self.setting_button.clicked.connect(self.show_settings)
        hselectlayout.addWidget(self.setting_button)

        vlayout.addLayout(hselectlayout)

        self.prompt_input = QPlainTextEdit(self)
        vlayout.addWidget(self.prompt_input)

        self.send_request_button = QPushButton("Send Request", self)
        vlayout.addWidget(self.send_request_button)

        self.answer_section = QTextEdit(self)
        self.answer_section.setReadOnly(True)
        vlayout.addWidget(self.answer_section)

        self.setLayout(vlayout)
        self.setWindowTitle('Chat Window')
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self.send_request_button.clicked.connect(self.send_request)

        # change theme
        self.setStyleSheet("""
    QWidget {
        background-color: #333; /* Dark background */
        color: #ffffff; /* acme-color-white */
    }
    QPlainTextEdit, QTextEdit {
        background-color: #2c2f33; /* Slightly lighter than main widget bg */
        border: 1px solid #3082ce; /* acme-color-primary */
        color: #ffffff; /* acme-color-white */
        padding: 5px;
    }
    QPushButton {
        background-color: #3082ce; /* acme-color-primary */
        color: white; /* acme-color-white */
        border-style: none;
        padding: 5px 10px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: lighter; /* Lighter version of primary color */
    }
    QPushButton:pressed {
        background-color: darker; /* Darker version of primary color */
    }
    QPushButton:focus {
        outline: none;
        border: 1px solid #4299e14c; /* acme-color-focusoutline */
    }
    QComboBox {
        background-color: #2c2f33; /* Slightly lighter than main widget bg */
        border: 1px solid #3082ce; /* acme-color-primary */
        color: #ffffff; /* acme-color-white */
        border-radius: 3px;
        padding: 1px 18px 1px 3px;
    }
    QComboBox::drop-down {
        subcontrol-position: center right;
        subcontrol-origin: padding;
        width: 15px;
        border-left-width: 1px;
        border-left-color: #3082ce; /* acme-color-primary */
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QLabel {
        margin: 5px;
        color: #cbd5e0; /* acme-color-gray300 */
    }
    QHBoxLayout {
        spacing: 10px;
    }
""")

    def load_prompts(self):
        # Retrieve prompts list from the settings window
        self.prompts_list = self.setting_window.get_prompts_list()

        # Clear any existing items in the combo box
        self.prompt_select_combo.clear()

        # Add the retrieved prompts to the combo box
        for prompt in self.prompts_list:
            self.prompt_select_combo.addItem(prompt)

    def load_streams(self):
        self.streams_list = self.setting_window.get_streams_list()
        self.stream_combo.clear()
        for stream in self.streams_list:
            self.stream_combo.addItem(stream)

    def send_request(self):
        # Use currentText() instead of text(), as QComboBox does not have text() method
        input_text = self.prompt_input.toPlainText()
        selected_prompt = self.prompt_select_combo.currentText()
        complete_text = f"{selected_prompt}: {input_text}"
        self.answer_section.append(f"Request Sent: {complete_text}")

    def show_settings(self):
        self.setting_window.show()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def set_prompt_text(self, text):
        self.prompt_input.setPlainText(text)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    chat_win = ChatWindow()
    chat_win.show()
    sys.exit(app.exec_())
