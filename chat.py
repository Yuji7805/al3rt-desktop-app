from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QTextEdit, QComboBox, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase
from setting import SettingWindow


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_window = SettingWindow()
        
        self.initUI()

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

    def send_request(self):
        input_text = self.prompt_input.text()
        self.answer_section.append(f"Request Sent: {input_text}")        

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
