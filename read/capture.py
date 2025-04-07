import pyautogui
import time

def get_board_region():
    # Get region of the board
    print("Move your mouse to the **TOP-LEFT** corner of the board...")
    time.sleep(3)
    top_left = pyautogui.position()
    print(f"Top-left: {top_left}")

    print("Now move your mouse to the **BOTTOM-RIGHT** corner of the board...")
    time.sleep(3)
    bottom_right = pyautogui.position()
    print(f"Bottom-right: {bottom_right}")

    return (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)

# Take screenshot of that region
def capture_board(output_file, region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("template/" + output_file)