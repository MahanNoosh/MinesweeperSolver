import pyautogui
import random

board_start = (0, 0)
tile_width = 0
tile_height = 0

def initialization_click(board, width, height):
    """
    Initializes the board_start, tile_width, and tile_height variables.
    
    Args:
        board (tuple): The board start position (x, y).
        width (int): The width of a tile.
        height (int): The height of a tile.
    """
    global board_start, tile_width, tile_height
    board_start = board[0], board[1]
    tile_width = width
    tile_height = height

def click_at(x, y):
    """
    Moves the mouse to (x, y) and performs a click.
    
    Args:
        x (int): The x-coordinate to click.
        y (int): The y-coordinate to click.
    """
    # Optional delay to move mouse smoothly
    # time.sleep(0.2)
    x = x + board_start[0] + tile_width // 2
    y = y + board_start[1] + tile_height // 2
    # Move the mouse to the given position and click
    pyautogui.moveTo(x, y)
    pyautogui.click()
    print(f"Clicked at ({x}, {y})")


def random_click(grid):
    col = random.randint(0, len(grid[0]) - 1)
    row = random.randint(0, len(grid) - 1)
    click_at(grid[row][col][0], grid[row][col][1])
    return row, col

def click_all(coordinates):
    for row, col in coordinates:
        click_at(row, col)


def flag_at(x, y):
    x = x + board_start[0] + tile_width // 2
    y = y + board_start[1] + tile_height // 2
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')

def flag_all(coordinates):
    for row, col in coordinates:
        flag_at(row, col)