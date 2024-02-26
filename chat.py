from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QTextEdit

import pyperclip
from setting import SettingWindow


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_window = SettingWindow()

        # Initialize UI
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        self.prompt_label = QLabel("Prompt Input")
        hlayout.addWidget(self.prompt_label)

        self.setting_button = QPushButton("Setting")
        self.setting_button.clicked.connect(self.show_settings)
        hlayout.addWidget(self.setting_button)

        vlayout.addLayout(hlayout)

        self.prompt_input = QTextEdit(self)
        vlayout.addWidget(self.prompt_input)

        self.send_request_button = QPushButton("Send Request", self)
        vlayout.addWidget(self.send_request_button)

        self.answer_section = QTextEdit(self)
        self.answer_section.setReadOnly(True)
        vlayout.addWidget(self.answer_section)

        # Set Layout and Window Title
        self.setLayout(vlayout)
        self.setWindowTitle('Chat Window')

        # Connect Button Clicks
        self.send_request_button.clicked.connect(self.send_request)

    def send_request(self):
        # Here you will call your logic for sending a request and updating the answer section
        input_text = self.prompt_input.text()
        self.answer_section.append(f"Request Sent: {input_text}")
        # TODO: Call your backend API or logic here

    def show_settings(self):
        self.setting_window.show()            

    def closeEvent(self, event):        
        self.hide()
        event.ignore()
        
    def set_prompt_text(self, text):
        self.prompt_input.setText(text)
        self.prompt_input.selectAll()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    chat_win = ChatWindow()
    chat_win.show()
    sys.exit(app.exec_())
