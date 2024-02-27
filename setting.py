from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                             QPushButton, QApplication, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import QSettings, pyqtSignal

import json
import requests

BACKEND_BASE = "https://main-monster-decent.ngrok-free.app/openai/"


# Define QSettings with your organization and application name
ORGANIZATION_NAME = 'MyOrganization'
APPLICATION_NAME = 'MyAppSettings'

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
    # Retrieve the JSON string from settings
    # Provide a default value of '{}'
    streams_json = {}
    global assistants
    assistants = fetch_data_from_url(
        ''.join([BACKEND_BASE, "assistants"]))

    for assistant in assistants["data"]:
        streams_json[assistant["name"]] = assistant['instructions']
    streams_json = json.dumps(streams_json)
    try:
        stream_dict = json.loads(streams_json)
        return stream_dict
    except json.JSONDecodeError:
        # Handle case where JSON is not decodable, return empty dict
        return {}


class SettingWindow(QWidget):
    prompts_updated = pyqtSignal()  # Define the signal
    streams_updated = pyqtSignal()

    def __init__(self):
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

        self.model_selection_label = QLabel("NLP Model Selection")
        layout.addWidget(self.model_selection_label)

        self.model_selection_combo = QComboBox(self)
        self.model_selection_combo.addItems(['Model 1', 'Model 2'])
        layout.addWidget(self.model_selection_combo)

        # Manage Streams Section
        self.manage_streams_label = QLabel("Streams")
        layout.addWidget(self.manage_streams_label)

        stream_layout = QHBoxLayout()
        self.stream_input = QLineEdit(self)
        stream_layout.addWidget(QLabel("Stream:"))
        stream_layout.addWidget(self.stream_input)

        self.instruction_input = QLineEdit(self)
        stream_layout.addWidget(QLabel("Instruction:"))
        stream_layout.addWidget(self.instruction_input)

        self.add_stream_btn = QPushButton("Add Stream", self)
        stream_layout.addWidget(self.add_stream_btn)
        layout.addLayout(stream_layout)

        self.stream_table = QTableWidget()
        self.stream_table.setColumnCount(3)
        self.stream_table.setHorizontalHeaderLabels(
            ["Stream", "Instruction", "Actions"])
        self.stream_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stream_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.stream_table)

        # Manage Prompts Section
        self.manage_prompts_label = QLabel("Prompts")
        layout.addWidget(self.manage_prompts_label)

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
        self.prompt_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prompt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.prompt_table)

        # Set Layout and Window Title
        self.setLayout(layout)
        self.setWindowTitle('Settings Window')

        # Connect Button Clicks
        self.add_stream_btn.clicked.connect(self.add_stream)
        self.add_prompt_btn.clicked.connect(self.add_prompt)

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
            delete_button = QPushButton('Delete')

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
        return [prompt for prompt, description in self._prompts_data.items()]

    def get_prompts_object(self):
        return self._prompts_data

    def delete_prompt(self, prompt):
        if prompt in self._prompts_data:
            del self._prompts_data[prompt]
            # Update the persistent storage
            store_prompts_table(self._prompts_data)
            self.update_table_with_prompts()

    def load_streams(self):
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
                        headers = {
                            "content-type": "application/json"
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

                headers = {
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
            btn_layout.setSpacing(2)  # Optional: Set spacing between buttons

            edit_button = QPushButton('Edit')
            delete_button = QPushButton('Delete')

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
        return [stream_name for stream_name, instruction in self._streams_data.items()]

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
                headers = {
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

    def closeEvent(self, event):
        self.prompts_updated.emit()
        self.streams_updated.emit()
        self.hide()
        event.ignore()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    setting_win = SettingWindow()
    setting_win.show()
    sys.exit(app.exec_())
