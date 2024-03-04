import signal
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import pyperclip
import keyboard
import threading
from pynput.mouse import Listener
import pyautogui
import pygetwindow as gw
import win32gui

# Import ChatWindow and SettingWindow classes from their respective files
from chat import ChatWindow
from setting import SettingWindow
# Define a handler for the SIGINT signal (usually generated by Ctrl+C)


def handle_sigint(sig, frame):
    print("SIGINT received, but application will not exit via Ctrl+C")


# Attach the SIGINT signal handler
signal.signal(signal.SIGINT, handle_sigint)


class TrayApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super(TrayApplication, self).__init__(*args, **kwargs)
        self.installEventFilter(self)


class SystemTrayApp:
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Register global hotkey
        keyboard.add_hotkey('ctrl+alt+x', self.show_chat)

        # Create instances of the windows but don't show them yet
        self.chat_window = ChatWindow()
        self.setting_window = SettingWindow()

        # Create a system tray icon, set an icon image (this should be a .png file located in your app directory)
        self.tray_icon = QSystemTrayIcon(QIcon('./assets/app.jpeg'), self.app)

        # Create a context menu for the tray icon
        self.tray_menu = QMenu()

        # Create actions for the context menu
        chat_action = QAction('Chat', self.app)
        chat_action.triggered.connect(self.show_chat)

        setting_action = QAction('Settings', self.app)
        setting_action.triggered.connect(self.show_settings)

        exit_action = QAction('Exit', self.app)
        exit_action.triggered.connect(self.exit_app)

        # Add actions to the tray menu
        self.tray_menu.addAction(chat_action)
        # self.tray_menu.addAction(setting_action)
        self.tray_menu.addSeparator()  # Separator line in the context menu
        self.tray_menu.addAction(exit_action)

        # Add the menu to the tray icon and show it
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.show_chat()

        # Start listening to mouse events
        # with Listener(on_click=self.on_click) as listener:
        #     listener.join()
        self.mouse_thread = threading.Thread(target=self.start_mouse_listener)
        self.mouse_thread.start()

    def start_mouse_listener(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def show_chat(self):
        print("clilcked......")
        text_to_send = self.copy_selected_text()
        self.chat_window.set_prompt_text(text_to_send)
        # Make sure the chat window is shown even if it was closed or hidden
        if self.chat_window.isHidden():
            self.chat_window.show()
        else:
            self.chat_window.activateWindow()

    def show_settings(self):
        self.setting_window.show()

    def exit_app(self):
        print(self.mouse_thread.is_alive())
        self.mouse_thread.join()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec_())

    # Function to find window by title
    def find_window_by_title(self, window_title):
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd == 0:
                print(f"Window '{window_title}' not found!")
                return None
            else:
                print(f"Found window '{window_title}', HWND: {hwnd}")
                return hwnd
        except Exception as e:
            print(e)
            return None

    def copy_selected_text(self):
        focused_window = gw.getActiveWindow()
        print("======start======")
        print(focused_window.title)
        print("====== end ======")
        if focused_window:
            try:
                selected_text = pyperclip.paste()
                return selected_text
            except Exception as e:
                print(f"Failed to retrieve selected text: {e}")
                return
        else:
            print("No active window detected")
            return

    def on_click(self, x, y, button, pressed):
        global start_x, start_y
        if pressed:
            start_x, start_y = x, y
        else:
            if start_x != x and start_y != y:
                pyautogui.hotkey('ctrl', 'c')
                selected_text = pyperclip.paste()
                print("Selected text:", selected_text)


def on_exit():
    # Remember to clean up the hotkey when the application exits
    keyboard.unhook_all_hotkeys()


if __name__ == '__main__':
    app = TrayApplication(sys.argv)
    tray_app = SystemTrayApp(app)
    app.aboutToQuit.connect(on_exit)
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, but application will not exit via Ctrl+C")
