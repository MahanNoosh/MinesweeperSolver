import pyautogui
import time

def get_board_region():
    """
    Prompts the user to move their mouse to the top-left and bottom-right corners of the board
    to determine the region for capturing the board.

    Returns:
        tuple: A region defined as (x, y, width, height).
    """
    print("Move your mouse to the **TOP-LEFT** corner of the board...")
    time.sleep(3)
    top_left = pyautogui.position()
    print(f"Top-left: {top_left}")

    print("Now move your mouse to the **BOTTOM-RIGHT** corner of the board...")
    time.sleep(3)
    bottom_right = pyautogui.position()
    print(f"Bottom-right: {bottom_right}")

    # Compute region as (x, y, width, height)
    region = (
        top_left.x,
        top_left.y,
        bottom_right.x - top_left.x,
        bottom_right.y - top_left.y
    )
    return region

def capture_board(output_file, region):
    """
    Captures a screenshot of the specified region and saves it to a file.

    Args:
        output_file (str): Name of the output image file (e.g., "state.png").
        region (tuple): Region to capture in the format (x, y, width, height).
    """
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("template/" + output_file)

def capture_tile(image, region):
    """
    Capture a tile from the image based on the given region.
    
    Args:
        image (PIL.Image): The image from which to capture the tile.
        region (tuple): The bounding box of the region (left, top, right, bottom).
    
    Returns:
        PIL.Image: The cropped tile image.
    """
    return image.crop(region)
