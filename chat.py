import os
import tempfile
import base64
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QPushButton, QTextEdit, QComboBox, QPlainTextEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QDesktopServices, QMovie
from PyQt5.QtCore import QUrl
from setting import SettingWindow
import requests
import json
import pyperclip
from PyQt5.QtCore import QSettings
import auth
from io import BytesIO
import requests
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QByteArray, Qt, QBuffer
from PyQt5.QtCore import QObject, pyqtSignal, QThread


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


settings_str = """
  <svg version="1.0" xmlns="http://www.w3.org/2000/svg"  width="64.000000pt" height="64.000000pt" viewBox="0 0 64.000000 64.000000"  preserveAspectRatio="xMidYMid meet">  <g transform="translate(0.000000,64.000000) scale(0.100000,-0.100000)" fill="#ffffff" stroke="none"> <path d="M200 614 c-53 -22 -55 -24 -51 -56 8 -75 9 -73 -29 -69 -19 2 -43 4 -53 5 -14 1 -25 -15 -42 -57 l-24 -57 40 -23 c21 -12 39 -29 39 -37 0 -8 -18 -25 -39 -37 l-40 -23 24 -57 c23 -56 25 -58 57 -54 75 8 73 9 69 -29 -2 -19 -4 -43 -5 -53 -1 -14 15 -25 57 -42 l57 -24 23 40 c12 21 29 39 37 39 8 0 25 -18 37 -39 l23 -40 57 24 c56 23 58 25 54 57 -8 75 -9 73 29 69 19 -2 43 -4 53 -5 14 -1 25 15 42 57 l24 57 -40 23 c-21 12 -39 29 -39 37 0 8 18 25 39 37 l40 23 -24 57 c-23 56 -25 58 -57 54 -75 -8 -73 -9 -69 29 2 19 4 43 5 53 1 14 -15 25 -57 42 l-57 24 -23 -40 c-23 -41 -52 -51 -61 -21 -4 9 -14 27 -24 38 l-17 21 -55 -23z m70 -59 c16 -27 28 -35 50 -35 22 0 34 8 50 35 24 39 28 40 65 23 29 -13 28 -12 15 -58 -8 -29 -7 -37 12 -57 12 -13 29 -21 37 -19 61 18 67 18 79 -9 17 -37 16 -41 -23 -65 -27 -16 -35 -28 -35 -50 0 -22 8 -34 35 -50 39 -24 40 -28 23 -65 -13 -29 -12 -28 -58 -15 -29 8 -37 7 -57 -12 -13 -12 -21 -29 -19 -37 18 -61 18 -67 -9 -79 -37 -17 -41 -16 -65 23 -30 49 -70 49 -100 0 -24 -39 -28 -40 -65 -23 -27 12 -27 18 -9 79 2 8 -6 25 -19 37 -20 19 -28 20 -57 12 -46 -13 -45 -14 -58 15 -17 37 -16 41 23 65 49 30 49 70 0 100 -39 24 -40 28 -23 65 12 27 18 27 79 9 8 -2 25 6 37 19 19 20 20 28 12 57 -13 46 -13 45 13 58 35 17 44 14 67 -23z"/> <path d="M263 420 c-34 -21 -63 -66 -63 -100 0 -54 65 -120 118 -120 57 0 122 64 122 120 0 56 -65 120 -122 120 -13 0 -37 -9 -55 -20z m112 -45 c50 -49 15 -135 -55 -135 -41 0 -80 39 -80 80 0 41 39 80 80 80 19 0 40 -9 55 -25z"/> </g> </svg> 
"""

copy_str = """
 <svg version="1.0" xmlns="http://www.w3.org/2000/svg"  width="24.000000pt" height="24.000000pt" viewBox="0 0 24.000000 24.000000"  preserveAspectRatio="xMidYMid meet">  <g transform="translate(0.000000,24.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> <path d="M17 223 c-4 -3 -7 -37 -7 -75 0 -53 4 -70 15 -75 9 -3 19 -2 23 2 4 4 1 10 -5 12 -9 3 -13 26 -13 64 l0 59 59 0 c38 0 61 -4 64 -12 2 -7 8 -10 12 -6 4 4 5 14 2 23 -5 11 -22 15 -75 15 -38 0 -72 -3 -75 -7z"/> <path d="M74 157 c-3 -8 -4 -43 -2 -78 l3 -64 75 0 75 0 0 75 0 75 -73 3 c-55 2 -74 -1 -78 -11z m136 -67 l0 -60 -60 0 -60 0 0 60 0 60 60 0 60 0 0 -60z"/> </g> </svg> 
"""

insert_str = """
 <svg version="1.0" xmlns="http://www.w3.org/2000/svg"  width="24.000000pt" height="24.000000pt" viewBox="0 0 24.000000 24.000000"  preserveAspectRatio="xMidYMid meet">  <g transform="translate(0.000000,24.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> <path d="M57 213 c-28 -14 -28 -15 -25 -106 l3 -92 83 -3 c68 -2 83 0 88 13 4 9 3 19 -1 23 -4 4 -10 1 -12 -5 -3 -9 -28 -13 -74 -13 l-69 0 0 80 c0 73 9 97 25 70 3 -5 24 -10 45 -10 21 0 42 5 45 10 10 17 25 11 25 -10 0 -11 5 -20 10 -20 6 0 10 11 10 24 0 47 -92 71 -153 39z m93 -13 c0 -5 -13 -10 -30 -10 -16 0 -30 5 -30 10 0 6 14 10 30 10 17 0 30 -4 30 -10z"/> <path d="M160 142 c0 -4 5 -13 12 -20 9 -9 3 -12 -30 -12 -23 0 -42 -4 -42 -10 0 -5 19 -10 41 -10 36 0 40 -2 29 -15 -23 -28 0 -30 27 -2 l27 26 -24 26 c-23 25 -40 32 -40 17z"/> </g> </svg> 
"""

app_str = """
 <svg  version="1.0" xmlns="http://www.w3.org/2000/svg"  width="291.000000pt" height="300.000000pt" viewBox="0 0 291.000000 300.000000"  preserveAspectRatio="xMidYMid meet">  <g transform="translate(0.000000,300.000000) scale(0.050000,-0.050000)" fill="#fe5b16" stroke="none"> <path d="M2177 5575 c-134 -45 -288 -176 -395 -337 l-101 -152 -145 1 c-421 1 -696 -261 -696 -664 l0 -199 -108 -61 c-420 -237 -540 -660 -292 -1033 62 -94 68 -113 43 -148 -286 -391 -176 -925 225 -1092 122 -51 132 -73 132 -282 0 -390 236 -626 649 -647 l219 -11 51 -101 c95 -187 158 -249 377 -372 169 -96 422 -64 629 78 114 78 138 80 223 15 36 -28 71 -50 78 -50 7 0 62 -22 122 -50 293 -134 692 42 852 376 l50 104 200 1 c387 2 650 259 669 655 l11 218 119 63 c410 217 503 630 241 1065 -38 64 -11 180 51 219 54 33 86 165 88 360 l1 202 -80 121 c-86 130 -226 258 -349 318 l-76 37 1 150 c2 467 -246 721 -706 721 l-173 0 -46 98 c-63 134 -246 317 -377 377 -226 104 -461 60 -748 -140 -29 -20 -44 -15 -90 28 -141 132 -457 196 -649 132z m486 -138 c166 -76 166 -72 15 -155 -67 -37 -168 -98 -225 -135 -100 -67 -107 -69 -253 -58 -82 6 -204 4 -270 -6 -66 -10 -123 -15 -127 -12 -13 12 90 177 135 217 23 21 42 49 42 63 0 13 16 30 35 37 19 6 76 34 125 61 139 77 342 72 523 -12z m942 31 c144 -49 403 -306 367 -365 -7 -11 -124 -17 -278 -15 l-267 5 -150 91 c-83 50 -169 97 -192 104 -59 19 -96 69 -71 94 100 100 416 146 591 86z m-610 -211 c13 -13 71 -47 129 -77 133 -68 158 -131 43 -106 -42 9 -196 15 -342 13 -293 -3 -298 -1 -185 79 160 113 297 149 355 91z m-1366 -276 c7 -10 -18 -66 -54 -125 -37 -58 -77 -128 -89 -156 -44 -101 -163 -212 -299 -279 -75 -37 -158 -85 -185 -105 -166 -127 -101 298 76 490 118 129 504 252 551 175z m490 0 c15 -9 -47 -52 -163 -111 -102 -52 -216 -121 -252 -152 -60 -53 -75 -61 -119 -57 -27 3 -3 63 79 201 l80 135 176 -1 c96 0 186 -7 199 -15z m1294 -1 c57 -9 141 -42 188 -73 124 -84 162 -107 466 -277 303 -171 301 -168 466 -487 49 -94 99 -184 112 -199 13 -15 66 -101 119 -191 l96 -163 0 -567 0 -568 -54 -102 c-30 -57 -66 -118 -81 -136 -15 -18 -43 -63 -63 -100 -226 -423 -330 -569 -450 -629 -56 -28 -172 -93 -257 -145 -86 -51 -171 -102 -190 -113 -19 -11 -100 -59 -178 -105 l-144 -85 -501 0 c-490 0 -676 17 -727 68 -34 33 -595 365 -658 389 -52 20 -177 150 -177 185 0 11 -17 44 -38 74 -21 30 -124 204 -230 386 l-192 333 0 561 c0 560 0 561 47 617 26 32 67 93 92 137 24 44 64 116 89 160 58 102 190 344 225 411 43 84 102 127 457 331 187 108 345 202 350 209 15 20 101 63 159 79 70 21 947 20 1074 0z m710 -110 c149 -233 139 -274 -36 -155 -64 44 -192 117 -283 163 -206 103 -196 125 51 118 l192 -6 76 -120z m361 89 c234 -62 396 -323 396 -640 0 -31 -93 -22 -120 11 -14 17 -33 30 -42 30 -89 0 -344 216 -402 340 -23 50 -64 124 -91 165 -91 137 -12 165 259 94z m151 -647 c52 -37 114 -73 137 -80 81 -25 132 -100 109 -160 -12 -30 -21 -108 -21 -173 0 -137 -20 -150 -67 -44 -42 94 -159 312 -175 325 -7 6 -27 38 -45 73 -18 35 -46 78 -64 95 -61 61 24 37 126 -36z m-3485 -175 c-62 -103 -132 -230 -156 -282 -63 -136 -74 -120 -74 105 l0 200 83 60 c46 33 91 60 102 60 10 0 42 18 70 41 100 78 91 8 -25 -184z m-314 -273 c6 -269 5 -272 -190 -602 -95 -161 -106 -164 -160 -47 -138 301 -98 538 127 742 64 58 130 119 147 134 57 57 70 17 76 -227z m4239 187 c229 -151 324 -353 292 -621 -29 -253 -135 -351 -212 -196 -64 128 -122 234 -137 246 -34 29 -61 111 -51 159 6 30 3 110 -6 177 -36 252 -6 314 114 235z m-4232 -703 c-3 -21 -7 -184 -7 -363 -1 -268 -6 -322 -28 -303 -36 29 -188 309 -188 345 0 27 116 237 159 287 12 13 21 39 21 57 0 18 11 28 25 24 14 -5 22 -26 18 -47z m4145 7 c7 -14 30 -52 52 -85 22 -33 64 -107 93 -164 l54 -103 -51 -77 c-28 -42 -70 -115 -94 -161 -70 -138 -82 -108 -82 204 0 158 -8 311 -19 338 -24 65 17 108 47 48z m309 -510 c147 -420 81 -663 -236 -868 -114 -74 -117 -73 -107 28 4 47 7 163 6 258 -3 170 51 344 120 387 11 7 20 28 20 48 0 35 133 222 158 222 7 0 24 -34 39 -75z m-4702 30 c18 -22 108 -185 203 -365 39 -74 60 -590 24 -590 -12 0 -22 8 -22 18 0 10 -20 23 -46 29 -123 31 -266 214 -333 426 -55 176 92 585 174 482z m395 -682 c14 -42 41 -92 58 -111 18 -19 32 -42 32 -51 0 -18 136 -247 175 -294 59 -71 -19 -55 -174 35 l-161 93 0 209 c0 223 22 260 70 119z m3887 -98 c-3 -80 1 -160 10 -178 13 -27 -14 -51 -131 -119 -80 -47 -162 -98 -181 -114 -54 -46 -72 25 -20 82 21 24 78 116 125 204 171 318 205 339 197 125z m-3861 -374 c41 -32 124 -81 184 -110 160 -76 207 -126 308 -327 50 -100 100 -187 111 -194 62 -38 12 -55 -128 -44 -345 26 -540 225 -566 579 -12 175 -10 177 91 96z m3839 -118 c-18 -262 -111 -401 -349 -521 -76 -38 -366 -64 -366 -33 0 5 35 65 77 135 43 69 101 168 131 220 42 75 84 113 197 178 80 46 176 105 215 131 102 69 107 63 95 -110z m-595 -191 c0 -25 -180 -327 -209 -351 -17 -14 -100 -20 -224 -17 l-197 6 68 40 c37 22 161 96 276 165 116 69 218 125 228 125 10 0 18 9 18 20 0 11 9 20 20 20 11 0 20 -3 20 -8z m-2542 -100 c56 -38 173 -107 262 -154 199 -106 199 -117 0 -121 -88 -2 -175 -4 -194 -5 -32 -2 -88 76 -185 252 -68 123 -36 130 117 28z m632 -374 c44 -12 94 -34 111 -49 17 -16 94 -62 170 -104 157 -86 168 -112 69 -164 -289 -151 -484 -130 -707 77 -99 92 -195 222 -181 244 15 26 443 22 538 -4z m900 2 c-7 -11 -50 -40 -96 -63 -46 -24 -112 -64 -146 -90 -83 -63 -117 -60 -258 25 -66 40 -140 80 -165 90 -114 43 -34 58 316 58 239 0 357 -7 349 -20z m739 2 c6 -9 -3 -29 -19 -42 -17 -14 -30 -36 -30 -50 0 -14 -54 -75 -119 -136 -207 -191 -399 -230 -663 -133 -209 76 -203 91 112 266 l200 111 254 1 c139 1 259 -7 265 -17z"/> <path d="M2520 4346 c-12 -64 -36 -165 -52 -226 -17 -60 -37 -141 -45 -180 -9 -38 -27 -90 -39 -114 -13 -24 -24 -67 -24 -96 0 -29 -10 -71 -22 -94 -12 -23 -30 -87 -39 -144 -31 -183 -52 -281 -75 -352 -57 -178 -84 -281 -84 -325 0 -26 -13 -65 -29 -86 -17 -22 -30 -69 -30 -105 -1 -36 -15 -93 -32 -127 -54 -103 -49 -226 9 -234 157 -22 206 27 242 242 12 69 33 170 48 225 l26 100 291 6 290 5 12 -125 c12 -122 23 -215 45 -350 11 -75 99 -111 219 -92 92 15 100 32 59 139 -35 91 -79 253 -109 397 -9 44 -28 112 -41 150 -13 39 -33 97 -44 130 -11 33 -28 101 -37 150 -22 125 -59 258 -91 336 -16 36 -28 85 -28 108 0 24 -9 71 -19 105 -19 59 -49 173 -102 381 -14 55 -30 141 -37 190 l-12 90 -113 6 -114 6 -23 -116z m150 -325 c17 -33 35 -116 42 -185 21 -246 121 -655 171 -699 74 -67 45 -77 -213 -77 -267 0 -280 6 -230 101 44 82 143 573 144 709 0 198 32 254 86 151z"/> <path d="M3468 4365 c6 -52 14 -389 17 -748 l5 -654 90 -8 c166 -16 165 -18 183 599 8 295 18 619 22 721 l7 185 -168 0 -168 0 12 -95z"/> <path d="M3521 2585 c-70 -57 -72 -231 -4 -287 118 -95 263 -16 263 144 0 156 -145 236 -259 143z"/> <path d="M1983 1755 c-65 -65 -15 -206 63 -177 34 13 110 14 217 2 119 -14 187 -13 245 5 62 18 81 18 87 -1 12 -34 115 -30 144 5 21 26 30 26 68 1 34 -22 104 -26 323 -20 517 16 624 16 644 4 33 -21 46 7 46 99 0 83 -2 86 -55 77 -47 -7 -477 -35 -565 -36 -16 0 -71 6 -122 15 -73 12 -98 8 -125 -19 -28 -28 -37 -29 -60 -6 -21 21 -119 28 -408 31 -210 3 -404 13 -431 23 -33 13 -56 12 -71 -3z"/> <path d="M4921 1125 c1 -37 81 -108 109 -98 43 17 37 44 -19 81 -53 34 -91 42 -90 17z"/> </g> </svg> 
"""

loading_base64 = """
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
"""

ORGANIZATION_NAME = 'AL3RT'
APPLICATION_NAME = 'AL3RT'

settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)

BACKEND_BASE = "https://al3rt.me/"


class Worker(QObject):
    # Signals to communicate with the main thread
    finished = pyqtSignal(str)  # Signal to send back the response
    error = pyqtSignal(Exception)  # Signal to send back any errors

    def __init__(self, url, headers, data):
        super().__init__()
        self.url = url
        self.headers = headers
        self.data = data

    def run(self):
        try:
            response = requests.post(
                self.url, headers=self.headers, data=self.data)
            if response.ok:
                gptAnswer = response.json()["content"][0]["text"]
                # Emit the successful response signal
                self.finished.emit(gptAnswer)
            else:
                response.raise_for_status()
        except Exception as e:
            self.error.emit(e)  # Emit the error signal


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_window = SettingWindow(self.load_streams)

        self.initUI()

        self.error_dialog = QMessageBox()

        self.auth = auth.LoginForm(self.enable_UI)
        self.load_prompts()

        self.load_streams()

        self.create_openai_thread()

        # Connect the signal to the slot
        self.setting_window.prompts_updated.connect(self.load_prompts)

    def initUI(self):
        self.previous_input = ''

        self.vlayout = QVBoxLayout(self)
        hselectlayout = QHBoxLayout()
        hcopyinsertlayout = QHBoxLayout()
        self.authLayout = QHBoxLayout()

        # Add sign in button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.show_auth)

        # Add sign out button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)

        self.authLayout.addStretch()
        self.authLayout.addWidget(self.logout_button)
        self.authLayout.addWidget(self.login_button)

        self.vlayout.addLayout(self.authLayout)

        self.stream_combo = QComboBox()
        self.stream_combo.setFixedHeight(24)
        hselectlayout.addWidget(self.stream_combo)

        self.prompt_select_combo = QComboBox()
        self.prompt_select_combo.setFixedHeight(24)
        self.prompt_select_combo.currentIndexChanged.connect(
            self.update_prompt_input)
        hselectlayout.addWidget(self.prompt_select_combo)

        self.setting_button = QPushButton(
            icon=svg_string_to_qicon(settings_str, (64, 64)))
        self.setting_button.setFixedWidth(22)
        self.setting_button.clicked.connect(self.show_settings)
        hselectlayout.addWidget(self.setting_button)

        self.vlayout.addLayout(hselectlayout)

        # input text
        self.prompt_input = QPlainTextEdit(self)
        self.vlayout.addWidget(self.prompt_input)

        self.send_request_button = QPushButton("Send Request", self)
        self.send_request_button.setFixedHeight(24)
        self.send_request_button.setCheckable(True)

        # Initial button style without background image
        self.original_style = self.send_request_button.styleSheet()

        # Decode the base64 string and write to a temporary file
        gif_data = base64.b64decode(loading_base64)
        self.temp_gif = tempfile.NamedTemporaryFile(
            suffix=".gif", delete=False)
        self.temp_gif.write(gif_data)
        self.temp_gif.flush()  # Ensure all data is written to disk

        # Set up the QMovie with the temporary file path
        self.movie = QMovie(self.temp_gif.name)
        # self.movie.start()
        # Slot for button click event
        # self.send_request_button.clicked.connect(self.toggle_background)

        self.vlayout.addWidget(self.send_request_button)

        self.copy_button = QPushButton()
        self.copy_button.setFixedWidth(22)
        self.copy_button.setIcon(svg_string_to_qicon(copy_str, (24, 24)))
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
        self.insert_button.setIcon(svg_string_to_qicon(insert_str, (24, 24)))
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
        self.vlayout.addLayout(hcopyinsertlayout)

        self.answer_section = QTextEdit(self)
        self.answer_section.setReadOnly(True)
        self.vlayout.addWidget(self.answer_section)

        self.setLayout(self.vlayout)
        self.setWindowTitle('Chat Window')
        self.setMinimumWidth(600)
        self.setMinimumHeight(550)

        self.send_request_button.clicked.connect(self.send_request)

        self.setWindowIcon(svg_string_to_qicon(app_str, (160, 160)))
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
        self.movie.frameChanged.connect(
            lambda: self.update_button_background(self.send_request_button))

    def toggle_background(self):
        try:
            if self.send_request_button.isChecked():
                try:
                    self.movie.start()
                except Exception as e:
                    print("Button error: ", e)
            else:
                self.movie.stop()
                self.send_request_button.setIcon(QIcon())
                self.send_request_button.setText("Send Request")
                self.send_request_button.setStyleSheet(self.original_style)
        except Exception as e:
            print("toggle error: ", e)

    def update_button_background(self, button):
        frame = self.movie.currentPixmap()
        frame = frame.scaledToHeight(
            int(self.send_request_button.height() / 2))
        button.setIcon(QIcon(frame))
        button.setIconSize(frame.size())
        button.setText("")

    def closeEvent(self, event):
        # Clean up: Delete the temporary file when closing the widget
        self.movie.stop()
        self.temp_gif.close()
        os.unlink(self.temp_gif.name)
        event.accept()

    def show_err_msg(self, msg):
        # Show Error Message Dialog
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setIcon(QMessageBox.Critical)
        self.error_dialog.setText(msg)
        self.error_dialog.exec_()

    def show_msg(self, msg):
        self.error_dialog.setIcon(QMessageBox.Information)
        self.error_dialog.setWindowTitle("Success")
        self.error_dialog.setText(msg)
        self.error_dialog.exec_()

    def show_auth(self):
        self.auth.setModal(True)
        self.auth.exec_()

    def open_backend_link(self):
        # Open the backend link in the default web browser
        backend_url = QUrl(BACKEND_BASE)
        QDesktopServices.openUrl(backend_url)

    def copy_answer(self):
        pyperclip.copy(self.answer_section.toPlainText())

    def load_prompts(self):
        # Retrieve prompts list from the settings window
        self.prompts_list = self.setting_window.get_prompts_list()

        # Clear any existing items in the combo box
        self.prompt_select_combo.clear()

        # Add the retrieved prompts to the combo box
        for prompt, desctiption in self.prompts_list:
            # show prompt name
            self.prompt_select_combo.addItem(prompt)

            # show prompt description
            # self.prompt_select_combo.addItem(desctiption)

    def load_streams(self):
        print("loading streams in chat")
        self.streams_list = self.setting_window.get_streams_list()
        if len(self.streams_list) == 0:
            self.disable_UI()
            self.show_err_msg("Please login to al3rt.me!")
            self.login_button.setVisible(True)
            self.logout_button.setVisible(False)
        else:
            self.login_button.setVisible(False)
            self.logout_button.setVisible(True)
            self.stream_combo.clear()
            for stream in self.streams_list:
                self.stream_combo.addItem(stream)

    def logout(self):
        print("logout called")
        access_token = settings.value('access_token', '')
        print(access_token)
        if len(access_token) == 0:
            return

        headers = {
            'Authorization': "Bearer " + access_token
        }
        print(headers)
        response = requests.get("https://al3rt.me/app/logout", headers=headers)
        print(response)
        if response.ok:
            self.login_button.setVisible(True)
            self.logout_button.setVisible(False)
            self.disable_UI()
            self.show_msg('Logged Out!\nAll actions are disabled.')
            return True
        return False

    def disable_UI(self):
        self.send_request_button.setDisabled(True)
        self.stream_combo.setDisabled(True)
        self.prompt_select_combo.setDisabled(True)
        self.setting_button.setDisabled(True)
        self.prompt_input.setDisabled(True)
        self.copy_button.setDisabled(True)

    def enable_UI(self):
        self.setting_window.load_streams()
        self.create_openai_thread()
        self.load_streams()
        self.load_prompts()
        self.send_request_button.setEnabled(True)
        self.stream_combo.setEnabled(True)
        self.prompt_select_combo.setEnabled(True)
        self.setting_button.setEnabled(True)
        self.prompt_input.setEnabled(True)
        self.copy_button.setEnabled(True)

    def update_prompt_input(self):
        # Get the currently selected prompt
        selected_prompt = self.prompt_select_combo.currentText()
        if selected_prompt:
            # show prompt name
            # prompts_object = self.setting_window.get_prompts_object()
            # prompt_description = prompts_object[selected_prompt]

            # show prompt description
            prompt_description = selected_prompt

            # Update the prompt input with the selected prompt and the current input text
            complete_text = f"{prompt_description}: {self.previous_input}"
            self.prompt_input.setPlainText(complete_text)

    def send_request(self):
        self.disable_UI()
        # Use currentText() instead of text(), as QComboBox does not have text() method
        prompt = self.prompt_input.toPlainText()
        if len(prompt) > 0:
            # self.toggle_background()
            self.movie.start()
            stream_name = self.stream_combo.currentText()
            asstId = self.setting_window.get_assistant_id(stream_name)

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

            # response = requests.post(''.join([BACKEND_BASE, 'openai/run']),
            #                             headers=headers, data=json.dumps(request))
            # print(response)
            # if response.ok:
            #     gptAnswer = response.json()["content"][0]["text"]
            #     self.answer_section.setText(gptAnswer)
            # else:
            #     response.raise_for_status()
            #     self.answer_section.setText(
            #         "Error: ", response.raise_for_status())
            # Create a QThread
            self.thread = QThread()
            # Create a worker object and move it to the new thread
            self.worker = Worker(
                ''.join([BACKEND_BASE, 'openai/run']), headers, json.dumps(request))
            self.worker.moveToThread(self.thread)
            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_request_finished)
            self.worker.error.connect(self.on_request_error)
            # Stop the thread when done
            self.worker.finished.connect(self.thread.quit)
            # Stop the thread on error
            self.worker.error.connect(self.thread.quit)

            # Start the thread which will start the worker
            self.thread.start()

    def on_request_finished(self, result):
        self.answer_section.setText(result)
        # Re-enable button after finishing
        self.send_request_button.setEnabled(True)
        self.movie.stop()
        self.send_request_button.setIcon(QIcon())
        self.send_request_button.setText("Send Request")
        self.send_request_button.setStyleSheet(self.original_style)
        self.enable_UI()

    def on_request_error(self, exception):
        self.show_err_msg(str(exception))
        self.send_request_button.setEnabled(
            True)  # Re-enable button after error
        self.movie.stop()
        self.send_request_button.setIcon(QIcon())
        self.send_request_button.setText("Send Request")
        self.send_request_button.setStyleSheet(self.original_style)
        self.enable_UI()

    def create_openai_thread(self):
        existingthread = settings.value("thdid")
        print("use existing thread: ", existingthread)
        if not str(existingthread).startswith("thread_"):
            try:
                url = "https://al3rt.me/app/openai/threads/create"
                # Assuming JSON content type
                access_token = settings.value('access_token', '')

                if len(access_token) == 0:
                    return

                headers = {
                    'Authorization': "Bearer " + access_token,
                    'Content-Type': 'application/json'
                }

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
