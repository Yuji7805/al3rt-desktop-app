import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
                             QPushButton, QApplication, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
import os
from win32com.client import Dispatch
import json
import requests

from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QByteArray, Qt


def svg_string_to_qicon(svg_string, size):
    # Create a QSvgRenderer from the SVG string
    renderer = QSvgRenderer(QByteArray(svg_string.encode()))

    # Create a QPixmap to render the SVG
    pixmap = QPixmap(size[0], size[1])
    # Fill the pixmap with a transparent background
    pixmap.fill(Qt.transparent)

    # Render the SVG onto the QPixmap
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    # Create a QIcon from the QPixmap
    icon = QIcon(pixmap)

    return icon


setting_str = """
 <svg version="1.0" xmlns="http://www.w3.org/2000/svg"  width="64.000000pt" height="64.000000pt" viewBox="0 0 64.000000 64.000000"  preserveAspectRatio="xMidYMid meet">  <g transform="translate(0.000000,64.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> <path d="M200 614 c-53 -22 -55 -24 -51 -56 8 -75 9 -73 -29 -69 -19 2 -43 4 -53 5 -14 1 -25 -15 -42 -57 l-24 -57 40 -23 c21 -12 39 -29 39 -37 0 -8 -18 -25 -39 -37 l-40 -23 24 -57 c23 -56 25 -58 57 -54 75 8 73 9 69 -29 -2 -19 -4 -43 -5 -53 -1 -14 15 -25 57 -42 l57 -24 23 40 c12 21 29 39 37 39 8 0 25 -18 37 -39 l23 -40 57 24 c56 23 58 25 54 57 -8 75 -9 73 29 69 19 -2 43 -4 53 -5 14 -1 25 15 42 57 l24 57 -40 23 c-21 12 -39 29 -39 37 0 8 18 25 39 37 l40 23 -24 57 c-23 56 -25 58 -57 54 -75 -8 -73 -9 -69 29 2 19 4 43 5 53 1 14 -15 25 -57 42 l-57 24 -23 -40 c-23 -41 -52 -51 -61 -21 -4 9 -14 27 -24 38 l-17 21 -55 -23z m70 -59 c16 -27 28 -35 50 -35 22 0 34 8 50 35 24 39 28 40 65 23 29 -13 28 -12 15 -58 -8 -29 -7 -37 12 -57 12 -13 29 -21 37 -19 61 18 67 18 79 -9 17 -37 16 -41 -23 -65 -27 -16 -35 -28 -35 -50 0 -22 8 -34 35 -50 39 -24 40 -28 23 -65 -13 -29 -12 -28 -58 -15 -29 8 -37 7 -57 -12 -13 -12 -21 -29 -19 -37 18 -61 18 -67 -9 -79 -37 -17 -41 -16 -65 23 -30 49 -70 49 -100 0 -24 -39 -28 -40 -65 -23 -27 12 -27 18 -9 79 2 8 -6 25 -19 37 -20 19 -28 20 -57 12 -46 -13 -45 -14 -58 15 -17 37 -16 41 23 65 49 30 49 70 0 100 -39 24 -40 28 -23 65 12 27 18 27 79 9 8 -2 25 6 37 19 19 20 20 28 12 57 -13 46 -13 45 13 58 35 17 44 14 67 -23z"/> <path d="M263 420 c-34 -21 -63 -66 -63 -100 0 -54 65 -120 118 -120 57 0 122 64 122 120 0 56 -65 120 -122 120 -13 0 -37 -9 -55 -20z m112 -45 c50 -49 15 -135 -55 -135 -41 0 -80 39 -80 80 0 41 39 80 80 80 19 0 40 -9 55 -25z"/> </g> </svg> 
"""

BACKEND_BASE = "https://al3rt.me/app/openai/"
# BACKEND_BASE = "http://localhost:5000/app/openai/"


# Define QSettings with your organization and application name
ORGANIZATION_NAME = 'AL3RT'
APPLICATION_NAME = 'AL3RT'

settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)

assistants = []


def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()  # Assuming the response is JSON-formatted
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}")  # Handle other possible errors


def store_prompts_table(prompt_dict):
    # Convert the dictionary to a JSON string for storage
    prompts_json = json.dumps(prompt_dict)
    # Store the JSON string in settings
    settings.setValue('prompts_table', prompts_json)
    settings.sync()  # Ensure data is written to persistent storage


def get_prompts_table():
    # Retrieve the JSON string from settings
    # Provide a default value of '{}'
    prompts_json = settings.value('prompts_table', '{}')
    # Convert the JSON string back to a dictionary
    try:
        prompt_dict = json.loads(prompts_json)
        return prompt_dict
    except json.JSONDecodeError:
        # Handle case where JSON is not decodable, return empty dict
        return {}


def store_streams_table(stream_dict):
    # Convert the dictionary to a JSON string for storage
    streams_json = json.dumps(stream_dict)
    # Store the JSON string in settings
    settings.setValue('streams_table', streams_json)
    settings.sync()  # Ensure data is written to persistent storage


def get_streams_table():
    print("get streams from al3rt...")
    # Retrieve the JSON string from settings
    # Provide a default value of '{}'
    streams_json = {}
    global assistants  # Include the CSRF token in the request headers
    access_token = settings.value('access_token', '')

    if len(access_token) == 0:
        return {}

    headers = {
        'Authorization': "Bearer " + access_token
    }

    response = requests.get(
        ''.join([BACKEND_BASE, "assistants"]), headers=headers)
    print(response)
    if response.status_code == 200:
        assistants = response.json()
        print(assistants)
        for assistant in assistants["data"]:
            streams_json[assistant["name"]] = assistant['instructions']
        streams_json = json.dumps(streams_json)
        try:
            stream_dict = json.loads(streams_json)
            return stream_dict
        except json.JSONDecodeError:
            # Handle case where JSON is not decodable, return empty dict
            return {}
    else:
        # Handle the case where the request fails
        return {}


class SettingWindow(QWidget):
    prompts_updated = pyqtSignal()  # Define the signal
    streams_updated = pyqtSignal()

    def __init__(self, callback):
        self.callback = callback
        super().__init__()
        self._prompts_data = {}  # Temporary in-memory storage for prompts
        self._streams_data = {}
        self.currently_editing_prompt = None
        self.currently_editing_stream = None
        # Initialize UI
        self.initUI()
        self.load_prompts()
        self.load_streams()

    def initUI(self):
        layout = QVBoxLayout()

        self.pin_to_taskbar_checkbox = QCheckBox("Desktop Shortcut")
        self.pin_to_taskbar_checkbox.toggled.connect(
            self.toggle_pin_to_taskbar)
        layout.addWidget(self.pin_to_taskbar_checkbox)

        self.model_selection_label = QLabel("NLP Model Selection")
        layout.addWidget(self.model_selection_label)

        self.model_selection_combo = QComboBox(self)
        self.model_selection_combo.addItems(['GPT-4'])
        self.model_selection_combo.addItems(['GPT-3.5'])
        self.model_selection_combo.addItems(['AI2'])
        self.model_selection_combo.addItems(['Claude'])
        self.model_selection_combo.addItems(['Gemini'])
        for index in range(self.model_selection_combo.count()):
            if self.model_selection_combo.itemText(index) in ['AI2', 'Claude', "Gemini"]:
                self.model_selection_combo.setItemData(
                    index, False, Qt.ItemDataRole.UserRole - 1)  # Disable the item

        layout.addWidget(self.model_selection_combo)

        # Manage Streams Section
        # self.manage_streams_label = QLabel("Streams")
        # layout.addWidget(self.manage_streams_label)

        stream_layout = QHBoxLayout()
        self.stream_input = QLineEdit(self)
        stream_layout.addWidget(QLabel("Stream:"))
        stream_layout.addWidget(self.stream_input)

        self.instruction_input = QLineEdit(self)
        stream_layout.addWidget(QLabel("Description:"))
        stream_layout.addWidget(self.instruction_input)

        self.add_stream_btn = QPushButton("Add Stream", self)
        stream_layout.addWidget(self.add_stream_btn)
        layout.addLayout(stream_layout)

        self.stream_table = QTableWidget()
        self.stream_table.setColumnCount(3)
        self.stream_table.setHorizontalHeaderLabels(
            ["Stream", "Description", "Actions"])
        self.stream_table.horizontalHeader().setStretchLastSection(True)
        self.stream_table.setColumnWidth(0, 150)
        self.stream_table.setColumnWidth(1, 180)
        self.stream_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stream_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.stream_table)

        # Manage Prompts Section
        # self.manage_prompts_label = QLabel("Prompts")
        # layout.addWidget(self.manage_prompts_label)

        prompt_layout = QHBoxLayout()
        self.prompt_input = QLineEdit(self)
        prompt_layout.addWidget(QLabel("Prompt:"))
        prompt_layout.addWidget(self.prompt_input)

        self.description_input = QLineEdit(self)
        prompt_layout.addWidget(QLabel("Description:"))
        prompt_layout.addWidget(self.description_input)

        self.add_prompt_btn = QPushButton("Add Prompt", self)
        prompt_layout.addWidget(self.add_prompt_btn)
        layout.addLayout(prompt_layout)

        self.prompt_table = QTableWidget(0, 3)

        self.prompt_table.setHorizontalHeaderLabels(
            ["Prompt", "Description", "Actions"])
        self.prompt_table.horizontalHeader().setStretchLastSection(True)
        self.prompt_table.setColumnWidth(0, 150)
        self.prompt_table.setColumnWidth(1, 180)

        self.prompt_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prompt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.prompt_table)

        # Set Layout and Window Title
        self.setLayout(layout)
        self.setWindowTitle('Settings Window')

        # Connect Button Clicks
        self.add_stream_btn.clicked.connect(self.add_stream)
        self.add_prompt_btn.clicked.connect(self.add_prompt)

        self.setWindowTitle("Setting")
        self.setWindowIcon(svg_string_to_qicon(setting_str, (64, 64)))

        stylesheet = """
            QWidget {
                background-color: #333;
                color: #ffffff;
                font-size: 11px;
            }
            QPlainTextEdit, QTextEdit {
                background-color: #2c2f33;
                border: 1px solid #3082ce;
                color: #ffffff;
                padding: 5px;
            }
            QPushButton {
                color: white;            
            }
            QPushButton:hover {
                background-color: lighter;
            }
            QPushButton:focus {
                outline: none;                
            }
            QComboBox {
                background-color: #2c2f33;
                border: 1px solid #3082ce;
                color: #ffffff;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
            }
            QComboBox::drop-down {
                subcontrol-position: center right;
                subcontrol-origin: padding;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #3082ce;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QLabel {
                margin: 5px;
                color: #cbd5e0;
            }
            QHBoxLayout {
                spacing: 10px;
            }
            QTableWidget {                
                background-color: #2c2f33; /* Slightly lighter than main widget bg */
                border: 1px solid #3082ce; /* Border color to match the primary color */
                gridline-color: #333; /* Grid line color to match the dark background */
            }

            QTableWidget::item {
                color: #ffffff; /* Font color */
                border-bottom: 1px solid #333; /* Bottom border color for items */
                padding: 5px; /* Padding inside cells */
            }

            QTableWidget::item:selected {
                background-color: #3082ce; /* Background color for selected item */
                color: white; /* Font color for selected item */
            }

            QHeaderView::section {
                background-color: #333; /* Background color for headers */
                color: #ffffff; /* Font color for headers */
                padding: 5px; /* Padding inside header cells */
                border-top: 0px; /* No top border for headers */
                border-bottom: 1px solid #3082ce; /* Border color to match the primary color */
                border-right: 1px solid #333; /* Right border color to match the dark background */
            }

            /* Header at the bottom if it exists */
            QTableWidget QTableCornerButton::section {
                background-color: #333; /* Background color for corner section */
                border: 0px;
            }
        """
        self.setStyleSheet(stylesheet)

    def get_executable_path(self):
        if getattr(sys, 'frozen', False):
            # The application is frozen (packaged)
            return sys.executable
        else:
            # The application is not frozen and is running as a regular Python script
            # In developer mode, return the path to your main script (.py file).
            return os.path.abspath(__file__.replace("setting", "main"))

    def toggle_pin_to_taskbar(self, checked):
        if checked:
            self.create_desktop_shortcut()
        else:
            self.remove_desktop_shortcut()
    
    def create_desktop_shortcut(self):
        desktop = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
        path = self.get_executable_path()
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(os.path.join(desktop, 'AL3RT.lnk'))
        shortcut.Targetpath = path
        shortcut.WorkingDirectory = os.path.dirname(path)
        shortcut.IconLocation = path
        shortcut.save()

    def remove_desktop_shortcut(self):
        desktop = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
        shortcut_path = os.path.join(desktop, 'AL3RT.lnk')
        try:
            os.remove(shortcut_path)
        except FileNotFoundError:
            pass  # Shortcut was already removed

    def load_prompts(self):
        # Load prompts from persistent storage
        self._prompts_data = get_prompts_table()
        self.update_table_with_prompts()

    def add_prompt(self):
        prompt_text = self.prompt_input.text()
        description_text = self.description_input.text()
        if prompt_text and description_text:
            # Update internal storage and table view
            self._prompts_data[prompt_text] = description_text
            store_prompts_table(self._prompts_data)  # Store updated data
            self.update_table_with_prompts()
            # Clear the input fields
            self.prompt_input.clear()
            self.description_input.clear()
        else:
            QMessageBox.warning(
                self, 'Error', 'Both Prompt and Description are required.')

    def update_table_with_prompts(self):
        self.prompt_table.setRowCount(0)  # Clear the table
        for prompt, description in self._prompts_data.items():
            row_position = self.prompt_table.rowCount()
            self.prompt_table.insertRow(row_position)
            self.prompt_table.setItem(
                row_position, 0, QTableWidgetItem(prompt))
            self.prompt_table.setItem(
                row_position, 1, QTableWidgetItem(description))

            # Create widget layout for Edit/Delete buttons
            widget = QWidget()
            btn_layout = QHBoxLayout()
            # Optional: Remove margins if preferred
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(2)  # Optional: Set spacing between buttons

            edit_button = QPushButton('Edit')
            edit_button.setFixedWidth(30)

            delete_button = QPushButton('Delete')
            delete_button.setFixedWidth(40)
            delete_button.setStyleSheet('background-color:"#e01111"')

            edit_button.clicked.connect(
                lambda _, p=prompt: self.edit_prompt(p))
            delete_button.clicked.connect(
                lambda _, p=prompt: self.delete_prompt(p))

            btn_layout.addWidget(edit_button)
            btn_layout.addWidget(delete_button)

            widget.setLayout(btn_layout)

            self.prompt_table.setCellWidget(row_position, 2, widget)

    def edit_prompt(self, prompt):
        description = self._prompts_data.get(prompt)
        if description is not None:
            # Populate the input fields with the existing data for editing
            self.prompt_input.setText(prompt)
            self.description_input.setText(description)
            # Set the currently editing prompt so we can remove it later if needed
            self.currently_editing_prompt = prompt

    def get_prompts_list(self):
        return [(prompt, description) for prompt, description in self._prompts_data.items()]

    def get_prompts_object(self):
        return self._prompts_data

    def delete_prompt(self, prompt):
        if prompt in self._prompts_data:
            del self._prompts_data[prompt]
            # Update the persistent storage
            store_prompts_table(self._prompts_data)
            self.update_table_with_prompts()

    def load_streams(self):
        print("getting streams table and setting")
        self._streams_data = get_streams_table()
        self.update_table_with_streams()

    def add_stream(self):
        stream_name = self.stream_input.text()
        instruction_text = self.instruction_input.text()
        if stream_name and instruction_text:
            # modify existing assistant
            if stream_name in self._streams_data:
                print("need to be modify")
                for assistant in assistants["data"]:
                    if assistant["name"] == stream_name:
                        asstId = assistant["id"]
                        _data_To_Modify_Assistant = {
                            "asstid": asstId,
                            "instruction": instruction_text,
                            "assist-name": stream_name,
                            "assist-type": "code_interpreter",
                        }
                        print(_data_To_Modify_Assistant)
                        access_token = settings.value('access_token', '')

                        if len(access_token) == 0:
                            return

                        headers = {
                            'Authorization': "Bearer " + access_token,
                            "content-type": "application/json",
                        }
                        response = requests.post(''.join(
                            [BACKEND_BASE, "assistants/modify"]), headers=headers, data=json.dumps(_data_To_Modify_Assistant))
                        if response.ok:
                            print('Success: Modified')
                            self._streams_data[stream_name] = instruction_text
                            # Store updated data
                            store_streams_table(self._streams_data)
                            self.update_table_with_streams()
                            self.stream_input.clear()
                            self.instruction_input.clear()
                        else:
                            # If response was unsuccessful, raise an exception
                            response.raise_for_status()

            # create new assistant
            else:
                _data_To_Create_Assistant = {
                    "instruction": instruction_text,
                    "assist-name": stream_name,
                    "assist-type": "code_interpreter",
                }
                access_token = settings.value('access_token', '')

                if len(access_token) == 0:
                    return

                headers = {
                    'Authorization': "Bearer " + access_token,
                    "content-type": "application/json"
                }
                response = requests.post(''.join(
                    [BACKEND_BASE, "assistants/create"]), headers=headers, data=json.dumps(_data_To_Create_Assistant))
                # Check if the request was successful and print the result
                if response.ok:
                    print('Success: Created Assistant')
                    print(response.text)
                    self._streams_data[stream_name] = instruction_text
                    # Store updated data
                    store_streams_table(self._streams_data)
                    self.update_table_with_streams()
                    self.stream_input.clear()
                    self.instruction_input.clear()
                else:
                    # If response was unsuccessful, raise an exception
                    response.raise_for_status()

            get_streams_table()
        else:
            QMessageBox.warning(
                self, 'Error', 'Both Stream and Instruction are required.')

    def update_table_with_streams(self):
        self.stream_table.setRowCount(0)  # Clear the table
        if self._streams_data != None:
            for stream_name, description in self._streams_data.items():
                row_position = self.stream_table.rowCount()
                self.stream_table.insertRow(row_position)
                self.stream_table.setItem(
                    row_position, 0, QTableWidgetItem(stream_name))
                self.stream_table.setItem(
                    row_position, 1, QTableWidgetItem(description))

                # Create widget layout for Edit/Delete buttons
                widget = QWidget()
                btn_layout = QHBoxLayout()
                # Optional: Remove margins if preferred
                btn_layout.setContentsMargins(0, 0, 0, 0)
                # Optional: Set spacing between buttons
                btn_layout.setSpacing(2)

                if stream_name == 'Default':
                    continue
                edit_button = QPushButton('Edit')
                edit_button.setFixedWidth(30)
                delete_button = QPushButton('Delete')
                delete_button.setFixedWidth(40)
                delete_button.setStyleSheet('background-color:"#e01111"')

                edit_button.clicked.connect(
                    lambda _, s=stream_name: self.edit_stream(s))
                delete_button.clicked.connect(
                    lambda _, s=stream_name: self.delete_stream(s))

                btn_layout.addWidget(edit_button)
                btn_layout.addWidget(delete_button)

                widget.setLayout(btn_layout)

                self.stream_table.setCellWidget(row_position, 2, widget)

    def edit_stream(self, stream_name):
        instruction = self._streams_data.get(stream_name)
        if instruction is not None:
            # Populate the input fields with the existing data for editing
            self.stream_input.setText(stream_name)
            self.instruction_input.setText(instruction)
            # Set the currently editing stream so we can remove it later if needed
            self.currently_editing_stream = stream_name

    def get_streams_list(self):
        if self._streams_data != None:
            return [stream_name for stream_name, instruction in self._streams_data.items()]
        else:
            return []

    def get_streams_object(self):
        return json.dumps(self._streams_data)

    def delete_stream(self, stream_name):
        # for assistant in assistants['data']:
        for assistant in assistants["data"]:
            if (assistant["name"] == stream_name):
                asstId = assistant["id"]
                payload = json.dumps({
                    "asstid": asstId
                })
                access_token = settings.value('access_token', '')

                if len(access_token) == 0:
                    return

                headers = {
                    'Authorization': "Bearer " + access_token,
                    "content-type": "application/json"
                }
                response = requests.delete(
                    ''.join([BACKEND_BASE, "assistants/delete"]), headers=headers, data=payload)
                if response.status_code == 200:
                    data = response.text
                    print(data)
                    if data == "deleted":
                        print("DELETING TABLE")
                        del self._streams_data[stream_name]
                        # Update the persistent storage
                        store_streams_table(self._streams_data)
                        # Refresh the UI
                        self.update_table_with_streams()
                        # table_stream.deleteRow(row.rowIndex) # This part refers to frontend operation which cannot be directly translated to Python
                    else:
                        print("Not found: ", asstId)
                else:
                    print(f"Error: {response.status_code}, {response.text}")

                # Handling exceptions from the requests library
                try:
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(e)

    def get_assistant_id(self, stream_name):
        try:
            for assistant in assistants["data"]:
                if assistant["name"] == stream_name:
                    return assistant["id"]
        except:
            print("Network error")

    def closeEvent(self, event):
        self.prompts_updated.emit()
        self.streams_updated.emit()
        self.hide()
        self.callback()
        event.ignore()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    setting_win = SettingWindow()
    setting_win.show()
    sys.exit(app.exec_())
