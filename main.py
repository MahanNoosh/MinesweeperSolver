import pyautogui
import time
from read.capture import capture_board

print("Move your mouse to the **TOP-LEFT** corner of the board...")
time.sleep(3)
top_left = pyautogui.position()
print(f"Top-left: {top_left}")

print("Now move your mouse to the **BOTTOM-RIGHT** corner of the board...")
time.sleep(3)
bottom_right = pyautogui.position()
print(f"Bottom-right: {bottom_right}")
# DO REFELECTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
region = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)

while True:
    capture_board(region)
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
