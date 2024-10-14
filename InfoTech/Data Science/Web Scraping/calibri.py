from pynput import mouse

# Variables to store the coordinates
variables = {
    "WebpageAck": None,
    "NullClick": None,
    "SaveWindow": None,
    "FilenameBox": None,
    "DirectoryBar": None,
    "SaveButton": None,
    "CloseWindow": None
}


# Function to print instructions and capture coordinates
def capture_coordinates(var_name):
    print(f"Please left-click to store the {var_name} coordinates, then right-click to move to the next.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def on_click(x, y, button, pressed):
    global current_var, current_clicks
    if pressed:
        if button == mouse.Button.left:
            variables[current_var] = (x, y)
            print(f"Coordinates for {current_var} recorded at: {x}, {y}")
        elif button == mouse.Button.right:
            print(f"Moving to the next variable.")
            return False


# Main function to iterate through all variables and capture their coordinates
def main():
    global current_var
    for var in variables:
        current_var = var
        capture_coordinates(var)

    print("All coordinates have been captured.")
    print(variables)


if __name__ == "__main__":
    main()
