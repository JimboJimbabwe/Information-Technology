import pyautogui
import time
import argparse

def perform_action_sequence(asset_value):
    # Left Click once at 995, 215
    pyautogui.click(x=995, y=215)
    time.sleep(0.5)
    # CTRL+A
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    # Right click at 1075, 261
    pyautogui.rightClick(x=1075, y=261)
    time.sleep(1)
    # Slowly move mouse from (1075, 261) to (1114, 543)
    pyautogui.moveTo(1075, 261)  # Ensure we start from the right-click position
    pyautogui.moveTo(1114, 563, duration=2)  # Slow movement over 2 seconds
    
    # Hover for 3 seconds
    time.sleep(3)
    # Left click at 1114, 543
    pyautogui.click()  # Click at the current position
    time.sleep(1.5)
    # Type asset_value + ".xml"
    pyautogui.write(f"{asset_value}.xml")
    time.sleep(0.5)
    # Left Click 1121,269
    pyautogui.click(x=1709, y=723)
    time.sleep(0.5)
    # Left Click 1715, 738 wait .05 seconds, click again
    pyautogui.click(x=1548, y=542)
    time.sleep(1)
    pyautogui.click(x=1904, y=52)
    time.sleep(1)
    pyautogui.click(x=1504, y=545)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Perform automated action sequence")
    parser.add_argument("--root_dir", help="Root directory (unused)")
    parser.add_argument("--business", help="Business name (unused)")
    parser.add_argument("--asset_type", help="Asset type (unused)")
    parser.add_argument("--asset_value", help="Asset value to be written", required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    print("The script will start in 5 seconds. Please ensure you're on the correct window.")
    time.sleep(5)
    perform_action_sequence(args.asset_value)
    print("Action sequence completed.")

if __name__ == "__main__":
    main()
