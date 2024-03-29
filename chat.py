from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QTextEdit, QComboBox, QPlainTextEdit
from PyQt5.QtGui import QIcon
from setting import SettingWindow
import requests
import json
import pyperclip
from PyQt5.QtCore import QSettings

ORGANIZATION_NAME = 'MyOrganization'
APPLICATION_NAME = 'MyAppSettings'

settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)

BACKEND_BASE = "https://main-monster-decent.ngrok-free.app/openai/"


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_window = SettingWindow()

        self.initUI()
        self.load_prompts()
        self.load_streams()

        self.create_openai_thread()

        # Connect the signal to the slot
        self.setting_window.prompts_updated.connect(self.load_prompts)

    def initUI(self):
        self.previous_input = ''

        vlayout = QVBoxLayout()
        hselectlayout = QHBoxLayout()
        hcopyinsertlayout = QHBoxLayout()

        self.stream_combo = QComboBox()
        self.stream_combo.setFixedHeight(24)
        hselectlayout.addWidget(self.stream_combo)

        self.prompt_select_combo = QComboBox()
        self.prompt_select_combo.setFixedHeight(24)
        self.prompt_select_combo.currentIndexChanged.connect(
            self.update_prompt_input)
        hselectlayout.addWidget(self.prompt_select_combo)

        self.setting_button = QPushButton(icon=QIcon("./assets/settings.png"))
        self.setting_button.setFixedWidth(22)
        self.setting_button.clicked.connect(self.show_settings)
        hselectlayout.addWidget(self.setting_button)

        vlayout.addLayout(hselectlayout)

        self.prompt_input = QPlainTextEdit(self)
        vlayout.addWidget(self.prompt_input)

        self.send_request_button = QPushButton("Send Request", self)
        vlayout.addWidget(self.send_request_button)

        self.copy_button = QPushButton()
        self.copy_button.setFixedWidth(22)
        self.copy_button.setIcon(QIcon("./assets/copy.png"))
        self.copy_button.setStyleSheet("QPushButton {\n"
                                       "    border: none;\n"
                                       "    border-radius: 10px;\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: #a0a0ab;\n"
                                       "    border-radius: 10px;\n"
                                       "}\n"
                                       "QPushButton:pressed {\n"
                                       "    background-color: #b3b3cc;\n"
                                       "    border-radius: 10px;\n"
                                       "}")
        self.copy_button.clicked.connect(self.copy_answer)

        self.insert_button = QPushButton()
        self.insert_button.setFixedWidth(22)
        self.insert_button.setIcon(QIcon("./assets/insert.png"))
        self.insert_button.setStyleSheet("QPushButton {\n"
                                         "    border: none;\n"
                                         "    border-radius: 10px;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: #a0a0ab;\n"
                                         "    border-radius: 10px;\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color: #b3b3cc;\n"
                                         "    border-radius: 10px;\n"
                                         "}")
        # self.insert_button.clicked.connect(self.insert_answer)

        hcopyinsertlayout.addWidget(self.copy_button)
        # hcopyinsertlayout.addWidget(self.insert_button)
        hcopyinsertlayout.addStretch()
        vlayout.addLayout(hcopyinsertlayout)

        self.answer_section = QTextEdit(self)
        self.answer_section.setReadOnly(True)
        vlayout.addWidget(self.answer_section)

        self.setLayout(vlayout)
        self.setWindowTitle('Chat Window')
        self.setMinimumWidth(600)
        self.setMinimumHeight(550)

        self.send_request_button.clicked.connect(self.send_request)

        self.setWindowIcon(QIcon("./assets/app.jpeg"))
        self.setWindowTitle("AL3RT CHAT")
        # change theme
        self.setStyleSheet("""
            QWidget {
                background-color: #333; /* Dark background */
                color: #ffffff; /* acme-color-white */
                font-size: 12px;
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
            # QPushButton:pressed {
            #     background-color: darker; /* Darker version of primary color */
            # }
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

    def copy_answer(self):
        pyperclip.copy(self.answer_section.toPlainText())

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

    def update_prompt_input(self):
        # Get the currently selected prompt
        selected_prompt = self.prompt_select_combo.currentText()
        if selected_prompt:
            prompts_object = self.setting_window.get_prompts_object()
            prompt_description = prompts_object[selected_prompt]
            # Update the prompt input with the selected prompt and the current input text
            complete_text = f"{prompt_description}: {self.previous_input}"
            self.prompt_input.setPlainText(complete_text)

    def send_request(self):
        # Use currentText() instead of text(), as QComboBox does not have text() method
        prompt = self.prompt_input.toPlainText()
        stream_name = self.stream_combo.currentText()
        asstId = self.setting_window.get_assistant_id(stream_name)
        if prompt.__len__() > 0:
            request = {
                "thdid": self.threadId,
                "asstid": asstId,
                "content": prompt,
            }

            print(request)
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }

            response = requests.post(''.join([BACKEND_BASE, 'run']),
                                     headers=headers, data=json.dumps(request))
            print(response)
            if response.ok:
                gptAnswer = response.json()["content"][0]["text"]
                self.answer_section.setText(gptAnswer)
            else:
                response.raise_for_status()
                self.answer_section.setText(
                    "Error: ", response.raise_for_status())

    def create_openai_thread(self):
        existingthread = settings.value("thdid")
        print("use existing thread: ", existingthread)
        if not str(existingthread).startswith("thread_"):
            try:
                url = "https://main-monster-decent.ngrok-free.app/openai/threads/create"
                # Assuming JSON content type
                headers = {'Content-Type': 'application/json'}

                response = requests.post(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes

                data = response.json()
                thdId = data["thdid"]
                self.threadId = thdId
                print("thread created: ", thdId)

                settings.setValue("thdid", thdId)
                settings.sync()

            except requests.RequestException as error:
                print(error)
        else:
            self.threadId = existingthread

    def show_settings(self):
        self.setting_window.show()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def set_prompt_text(self, text):
        self.previous_input = text
        self.prompt_input.setPlainText(text)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    chat_win = ChatWindow()
    chat_win.show()
    sys.exit(app.exec_())
