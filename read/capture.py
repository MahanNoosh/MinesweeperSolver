import pyautogui

# Take screenshot of that region
def capture_board(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("template/state.png")
def captue_tile(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("template/tile.png")
