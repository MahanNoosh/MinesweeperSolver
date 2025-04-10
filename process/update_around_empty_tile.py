from read.get_tile_number import get_tile_number
from read.get_tile_region import get_tile_region
from read.capture import capture_tile
from PIL import Image
from collections import deque

def update_around_empty_tile(i_row, i_col, grid, grid_coordinates):
    """
    Update the surrounding tiles of an empty tile in the grid.
    
    Args:
        i_row (int): The row index of the empty tile.
        i_col (int): The column index of the empty tile.
        grid (list): The 2D grid representing the game board.
        grid_coordinates (list): The coordinates of each tile in the grid.
    """
    def is_within_bounds(row, col):
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    def process_tile(row, col):
        if grid[row][col] is None:
            image = Image.open("template/state.png")
            tile = capture_tile(image, get_tile_region(row, col, grid_coordinates))
            number = get_tile_number(tile)
            grid[row][col] = number if number else 0
            return not number  # Return True if the tile is empty (number is 0)
        return False

    queue = deque([(i_row, i_col)])
    while queue:
        row, col = queue.popleft()
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row == 0 and d_col == 0:
                    continue
                new_row, new_col = row + d_row, col + d_col
                if is_within_bounds(new_row, new_col) and process_tile(new_row, new_col):
                    queue.append((new_row, new_col))
