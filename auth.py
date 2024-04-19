import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import requests
from bs4 import BeautifulSoup
import setting


class LoginForm(QDialog):
    def __init__(self, callback):
        self.callback = callback
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(260, 350)

        layout = QVBoxLayout()

        # Show msg
        self.msg = QMessageBox()

        # Logo and Title
        logo_label = QLabel(self)
        pixmap = QPixmap('./assets/icon3.png')
        pixmap = pixmap.scaled(120, 115)  # Set the image size to 120x115
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        title_label = QLabel('Login', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username Input
        username_label = QLabel('Username', self)
        layout.addWidget(username_label)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        # Password Input
        password_label = QLabel('Password', self)
        layout.addWidget(password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Show Password Checkbox
        show_password_checkbox = QCheckBox('Show Password', self)
        show_password_checkbox.stateChanged.connect(
            self.toggle_password_visibility)
        layout.addWidget(show_password_checkbox)

        # Login Button
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Account Management Links
        account_links_layout = QHBoxLayout()

        # go to al3rt.me to register
        register_link = QLabel(
            '<a href="https://al3rt.me/register">Register here</a>', self)
        # Open link in the default web browser
        register_link.setOpenExternalLinks(True)
        # Connect the linkActivated signal to a slot
        register_link.linkActivated.connect(self.open_link)

        reset_link = QLabel(
            '<a href="https://al3rt.me/reset">Forgot Password?</a>', self)
        # Open link in the default web browser
        reset_link.setOpenExternalLinks(True)
        # Connect the linkActivated signal to a slot
        reset_link.linkActivated.connect(self.open_link)

        account_links_layout.addWidget(register_link)
        account_links_layout.addStretch()
        account_links_layout.addWidget(reset_link)
        layout.addLayout(account_links_layout)

        self.setLayout(layout)

    def open_link(self, url):
        # Open the URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        username = "Yuji Koyama"
        password = "qweqweqwe"
        # Send a POST request to the Flask backend's /login endpoint
        # url = 'http://localhost:5000/app/login'
        url = 'https://al3rt.me/app/login'
        data = {'username': username, 'password': password}
        try:
            response = requests.post(url, data=data)
            print(response)
            if response.status_code == 200:
                data = response.json()
                print(data)
                access_token = data['access_token']
                print(access_token)
                setting.settings.setValue("access_token", access_token)
                setting.settings.sync()

                self.msg.setWindowTitle("Success")
                self.msg.setText(data['message'])
                self.msg.exec_()
                # enable UI
                self.callback()
                
                self.close()
            else:
                # Login failed, display an error message
                print("Login failed")

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())
