from pynput.mouse import Listener

start_x = None
start_y = None


def on_click(x, y, button, pressed):
    action = 'Pressed' if pressed else 'Released'
    global start_x, start_y
    if pressed:
        start_x, start_y = x, y
    else:
        if start_x != x and start_y != y:
            on_select(start_x, start_y, x, y)


def on_select():
    print("Text selected")


# Start listening to mouse events
with Listener(on_click=on_click) as listener:
    listener.join()
