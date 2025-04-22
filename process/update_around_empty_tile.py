from read.get_tile_number import get_tile_number
from process.get_tile_region import get_tile_region
from read.capture import capture_tile, capture_board
from PIL import Image
from collections import deque

def update_around_empty_tile(i_row, i_col, solver, board_img, tile_regions):
    """
    Update all cells around an empty (zero) tile.
    
    Args:
        i_row (int): Row index of the empty tile
        i_col (int): Column index of the empty tile
        solver (SolverLogic): The solver instance
        grid_coordinates (list): List of tile coordinates
        board_region (tuple): The board region (x, y, width, height)
    """
    def is_within_bounds(row, col):
        return 0 <= row < len(solver.grid) and 0 <= col < len(solver.grid[0])

    def process_tile(row, col):
        # Skip if cell is already processed
        if solver.grid[row][col].value is not None:
            return False
            
        try:
            tile = capture_tile(board_img, tile_regions[row][col])
            number = get_tile_number(tile)
            print(f"Tile at ({row}, {col}) has number: {number}")
            value = int(number) if number else 0
            solver.update_cell(row, col, value)
            print(f"Updated cell ({row}, {col}) with value {value}")
            return value == 0  # Continue if this is also a zero
        except Exception as e:
            print(f"Error processing tile at ({row}, {col}): {str(e)}")
            return False


    # Use BFS to process all connected zero tiles
    queue = deque([(i_row, i_col)])
    visited = set([(i_row, i_col)])

    while queue:
        row, col = queue.popleft()
        print(f"Processing neighbors of cell ({row}, {col})")
        
        # Process all 8 neighbors
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
