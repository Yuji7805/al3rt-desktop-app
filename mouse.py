from pynput.mouse import Listener


def on_move(x, y):
    print(f'Mouse moved to ({x}, {y})')


def on_click(x, y, button, pressed):
    action = 'Pressed' if pressed else 'Released'
    global start_x, start_y
    if pressed:
        start_x, start_y = x, y
    else:
        on_select(start_x, start_y, x, y)
    # print(action)
    # print(f'Mouse {action} at ({x}, {y}) with {button}')


def on_select(x1, y1, x2, y2):
    print("Text selected")


# Variables to store the starting and ending positions of the selection
start_x, start_y = None, None


# Start listening to mouse events
with Listener(on_click=on_click) as listener:
    listener.join()
