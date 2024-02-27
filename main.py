import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QGuiApplication, QClipboard
import pyperclip

import win32clipboard
import keyboard

# Import ChatWindow and SettingWindow classes from their respective files
from chat import ChatWindow
from setting import SettingWindow
import win32gui
import win32api
import win32con


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
        self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), self.app)

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
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec_())

    # Function to send a key press event to the window
    # Function to send Ctrl+C to the window

    def send_ctrl_c(self, hwnd):
        try:
            import time
            # Bring the window to the foreground
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)  # Add a small delay to allow the window to come to the foreground
            
            # Press down the 'Ctrl' key
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)

            # Press and release the 'C' key
            win32api.keybd_event(0x43, 0, 0, 0)              # Down 'C'
            time.sleep(0.05)  # Add a slight delay between pressing and releasing the key
            win32api.keybd_event(
                0x43, 0, win32con.KEYEVENTF_KEYUP, 0)  # Up 'C'

            # Release the 'Ctrl' key
            win32api.keybd_event(win32con.VK_CONTROL, 0,
                                    win32con.KEYEVENTF_KEYUP, 0)

            print(f"Sent Ctrl+C to HWND: {hwnd}")
        except Exception as e:
            print(e)

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
        import pygetwindow as gw
        focused_window = gw.getActiveWindow()
        print("======start======")
        print(focused_window.title)
        print("====== end ======")
        if focused_window:
            print(type(focused_window.title))
            window_title = focused_window.title

            hwnd = self.find_window_by_title(window_title=window_title)
            
            self.send_ctrl_c(hwnd)
            try:
                selected_text = pyperclip.paste()
                pyperclip.copy("")
                return selected_text                
            except Exception as e:
                print(f"Failed to retrieve selected text: {e}")
                return
        else:
            print("No active window detected")
            return 


class TrayApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super(TrayApplication, self).__init__(*args, **kwargs)
        self.installEventFilter(self)


def on_exit():
    # Remember to clean up the hotkey when the application exits
    keyboard.unhook_all_hotkeys()


if __name__ == '__main__':
    import signal

    # Define a handler for the SIGINT signal (usually generated by Ctrl+C)
    def handle_sigint(sig, frame):
        print("SIGINT received, but application will not exit via Ctrl+C")

    # Attach the SIGINT signal handler
    signal.signal(signal.SIGINT, handle_sigint)

    app = TrayApplication(sys.argv)
    tray_app = SystemTrayApp(app)
    app.aboutToQuit.connect(on_exit)

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, but application will not exit via Ctrl+C")
