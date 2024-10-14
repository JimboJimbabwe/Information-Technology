import pyautogui
import time
import argparse

def perform_action_sequence(asset_value):
    # Click at 11, 15
    pyautogui.click(x=11, y=15)
    time.sleep(0.5)
    # Type "bur"
    pyautogui.write("bur")
    time.sleep(0.5)
    # Hit enter twice
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.click(x=1026, y=501)
    time.sleep(0.5)
    pyautogui.click(x=1149, y=570)
    time.sleep(2.5)
    # Click at 1277, 746 twice
    pyautogui.click(x=1277, y=746, clicks=2, interval=1.1)
    time.sleep(5.5)
    # Click 1080, 92
    pyautogui.click(x=1080, y=92)
    time.sleep(1.5)
    # Click 1065, 139
    pyautogui.click(x=1065, y=139)
    time.sleep(3.5)
    # Click 1050, 303
    pyautogui.click(x=1050, y=303)
    time.sleep(3.5)
    # Click 1332, 494
    pyautogui.click(x=1332, y=494)
    time.sleep(3.5)
    # Type the asset_value URL
    if not asset_value.startswith(('http://', 'https://')):
        asset_value = 'https://' + asset_value
    pyautogui.write(asset_value)
    time.sleep(1.5)
    # Hit enter
    pyautogui.press('enter')
    time.sleep(1)  # Longer wait time for page to load
    # Click at 1528, 557
    pyautogui.click(x=1528, y=557)
    time.sleep(0.5)
    # Click at 1145, 91
    pyautogui.click(x=1145, y=91)
    time.sleep(0.5)
    # Click at 1078, 137
    pyautogui.click(x=1078, y=137)
    time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="Perform automated browser actions")
    parser.add_argument("--asset_value", required=True, help="URL to be entered in the browser")
    args = parser.parse_args()

    print("The script will start in 5 seconds. Please ensure you're on the correct window.")
    time.sleep(5)
    perform_action_sequence(args.asset_value)
    print("Action sequence completed.")

if __name__ == "__main__":
    main()
