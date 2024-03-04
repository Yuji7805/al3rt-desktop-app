from pynput.mouse import Listener
import pyperclip

start_x = None
start_y = None


def on_click(x, y, button, pressed):
    global start_x, start_y
    if pressed:
        start_x, start_y = x, y
    else:
        if start_x != x and start_y != y:
            on_select()


def on_select():
    import pyautogui

    pyautogui.hotkey('ctrl', 'c')

    selected_text = pyperclip.paste()
    print("Selected text:", selected_text)


# Start listening to mouse events
with Listener(on_click=on_click) as listener:
    listener.join()
