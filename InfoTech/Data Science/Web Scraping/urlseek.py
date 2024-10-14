import pyautogui
import time
import pyperclip

def get_click_coordinates():
    print("Please move your mouse to the URL bar and press the left mouse button.")
    print("You have 5 seconds to position your mouse.")
    time.sleep(5)  # Give user time to position the mouse
    print("Recording mouse position now...")
    return pyautogui.position()

def process_urls(url_file_name, url_coords):
    with open(url_file_name, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        
        # Copy URL to clipboard
        pyperclip.copy(url)
        
        # Double click the URL bar
        pyautogui.click(url_coords.x, url_coords.y, clicks=2, interval=0.1)
        time.sleep(0.5)
        
        # Paste the URL
        pyautogui.hotkey('ctrl', 'v')  # Use 'command' instead of 'ctrl' on Mac
        time.sleep(0.5)
        
        # Hit enter twice
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Double click the URL bar again
        pyautogui.click(url_coords.x, url_coords.y, clicks=2, interval=0.1)
        
        # Clear the URL bar
        pyautogui.hotkey('ctrl', 'a')  # Select all
        pyautogui.press('delete')  # Delete selected text
        
        # Wait a bit before the next iteration
        time.sleep(1)

def main():
    # Get the URL bar coordinates
    url_coords = get_click_coordinates()
    print(f"Recorded coordinates: {url_coords}")

    # File name of the URL list in the same directory
    url_file_name = "endpoints.txt"

    # Process the URLs
    process_urls(url_file_name, url_coords)

if __name__ == "__main__":
    main()
