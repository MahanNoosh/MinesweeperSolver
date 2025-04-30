from read.get_tile_number import get_tile_number
from process.get_tile_region import get_tile_region
from read.capture import capture_tile, capture_board
from PIL import Image
from collections import deque

def update_around_empty_tile(i_row, i_col, solver, board_img, tile_regions):
    """
    Update all cells around an empty (zero) tile that are visible (opened).
    Stop recursion when a number tile is found.
    """
    def is_within_bounds(row, col):
        return 0 <= row < len(solver.grid) and 0 <= col < len(solver.grid[0])

    def process_tile(row, col):
        # Skip if already known
        if solver.grid[row][col].value is not None:
            return False

        try:
            tile_img = capture_tile(board_img, tile_regions[row][col])
            number = get_tile_number(tile_img)

            # If it's not visibly opened (number is None or ''), do not process it
            if number is None or number == '':
                print(f"Tile at ({row}, {col}) is not visibly open, skipping.")
                return False

            value = int(number)
            solver.update_cell(row, col, value)
            print(f"Updated cell ({row}, {col}) with value {value}")
            return value == 0  # Continue recursion only if this tile is also empty
        except Exception as e:
            print(f"Error processing tile at ({row}, {col}): {str(e)}")
            return False

    # BFS to reveal only connected visibly opened empty tiles
    queue = deque([(i_row, i_col)])
    visited = set([(i_row, i_col)])

    while queue:
        row, col = queue.popleft()
        print(f"Processing neighbors of cell ({row}, {col})")

        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row == 0 and d_col == 0:
                    continue

                new_row, new_col = row + d_row, col + d_col
                if is_within_bounds(new_row, new_col) and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    if process_tile(new_row, new_col):
                        queue.append((new_row, new_col))
                        print(f"Added cell ({new_row}, {new_col}) to queue")
