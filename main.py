from read.capture import capture_board, get_board_region, capture_tile
from read.get_starter_template import get_starter_template
from read.detect_grid_intersections_on_board import detect_grid_intersections_on_board
from process.convert_to_2d_tiles_coordinate_list import find_list_dimension, convert_to_2d_tiles_list
from write.click import *
from read.read_board_numbers import read_board_numbers
from read.get_tile_number import *
from process.get_tile_region import *
from process.update_around_empty_tile import update_around_empty_tile
from solver.solver_logic import SolverLogic
from PIL import Image
import os
import time
import cv2
import numpy as np


if not os.path.exists('template'):
    os.mkdir('template')

board_region = get_board_region()

capture_board("state.png", board_region)
get_starter_template("state.png", "default_tile1.png", "default_tile2.png")
intersections = detect_grid_intersections_on_board("state.png", "intersection1.png", "intersection2.png")
row, col = find_list_dimension(intersections)
grid_coordinates = convert_to_2d_tiles_list(intersections)
tile_width = grid_coordinates[0][1][0] - grid_coordinates[0][0][0]
tile_height = grid_coordinates[1][0][1] - grid_coordinates[0][0][1]
initialize_tile_dimensions(tile_width, tile_height)

solver = SolverLogic(row, col)
tile_regions = get_all_tile_regions(grid_coordinates)

def update_board_state(r: int, c: int) -> bool:
    """Update the board state after a move.
    
    Args:
        r: Row index
        c: Column index
        
    Returns:
        bool: True if the update was successful, False if the game is over
    """
    try:
        capture_board("state.png", board_region)
        image = Image.open("template/state.png")
        number = get_tile_number(capture_tile(image, tile_regions[r][c]))
        
        # Check if we hit a mine
        if number == 'X' or number == 'x':
            print(f"Hit a mine at ({r}, {c})!")
            solver.update_cell(r, c, -1)  # Use update_cell instead of direct assignment
            return False
            
        # If we got a number, update the cell value
        if number != '':
            value = int(number)
            solver.update_cell(r, c, value)
            print(f"Updated cell ({r}, {c}) with value {value}")
        else:    
            # Process empty tiles
            solver.update_cell(r, c, 0)
            update_around_empty_tile(r, c, solver, grid_coordinates, board_region)
            
        return True
    except Exception as e:
        print(f"Error updating board state: {str(e)}")
        return False

def make_move(r: int, c: int, is_flag: bool = False) -> bool:
    """Make a move on the board.
    
    Args:
        r: Row index
        c: Column index
        is_flag: Whether to flag the cell instead of clicking it
        
    Returns:
        bool: True if the move was successful, False if the game is over
    """
    try:
        # Skip if the cell is already revealed (unless we're flagging)
        if not is_flag and solver.grid[r][c].value is not None:
            print(f"Skipping already revealed cell ({r}, {c})")
            return True
            
        # For flagging, skip if already flagged
        if is_flag and solver.grid[r][c].is_flagged:
            print(f"Skipping already flagged cell ({r}, {c})")
            return True
            
        if is_flag:
            print(f"Flagging cell ({r}, {c})")
            flag_at(grid_coordinates[r][c][0], grid_coordinates[r][c][1])
            time.sleep(0.3)  # Increased delay after flagging
            solver.update_cell(r, c, -1)
        else:
            print(f"Clicking cell ({r}, {c})")
            click_at(grid_coordinates[r][c][0], grid_coordinates[r][c][1])
            time.sleep(0.5)  # Increased delay after clicking
            
            # Update board state after clicking
            capture_board("state.png", board_region)
            image = Image.open("template/state.png")
            number = get_tile_number(capture_tile(image, tile_regions[r][c]))
            
            # Check if we hit a mine
            if number == 'X' or number == 'x':
                print(f"Hit a mine at ({r}, {c})!")
                solver.update_cell(r, c, -1)  # Use update_cell instead of direct assignment
                return False
                
            # If we got a number, update the cell value
            if number != '':
                value = int(number)
                solver.update_cell(r, c, value)
                print(f"Updated cell ({r}, {c}) with value {value}")
            else:    
                # Process empty tiles
                solver.update_cell(r, c, 0)
                print(f"Processing zero cell at ({r}, {c})")
                update_around_empty_tile(r, c, solver, grid_coordinates, board_region)
                
        return True
    except Exception as e:
        print(f"Error making move: {str(e)}")
        return False

def check_game_state() -> bool:
    """Check if the game is still in progress.
    
    Returns:
        bool: True if the game should continue, False if it's over
    """
    # Check if all non-mine cells are revealed
    for r in range(row):
        for c in range(col):
            cell = solver.grid[r][c]
            if not cell.is_mine and cell.value is None:
                return True
    return False

# Make first move
initialization_click(board_region, tile_width, tile_height)
guess_set = solver.make_educated_guess()
if guess_set:
    # Convert set to tuple
    r, c = next(iter(guess_set))
    print(f"Guessing cell ({r}, {c}) with probability {solver.grid[r][c].probability:.2f}")
    if not make_move(r, c):
        print("Game over - hit a mine while making educated guess")
        exit(1)
# Main solving loop
max_iterations = 100
for iteration in range(max_iterations):
    print(f"\nIteration {iteration + 1}")
    
    # Always check for mines first
    mines = solver.find_certain_mines()
    if mines:
        print(f"Found {len(mines)} certain mines")
        for r, c in mines:
            print(f"Flagging mine at ({r}, {c})")
            if not make_move(r, c, is_flag=True):
                print("Game over - hit a mine while flagging")
                exit(1)
        # After flagging mines, check for safe moves
        continue
    
    # Only proceed to safe moves if no mines are found
    safe_moves = solver.find_safe_moves()
    if safe_moves:
        print(f"Found {len(safe_moves)} safe moves")
        for r, c in safe_moves:
            if not make_move(r, c):
                print("Game over - hit a mine while making safe move")
                exit(1)
        # After making safe moves, go back to check for mines
        continue
    
    # Make educated guess only if no mines or safe moves
    print("No certain moves available, making educated guess")
    guess_set = solver.make_educated_guess()
    if guess_set and not safe_moves and not mines:
        # Convert set to tuple
        r, c = next(iter(guess_set))
        print(f"Guessing cell ({r}, {c}) with probability {solver.grid[r][c].probability:.2f}")
        if not make_move(r, c):
            print("Game over - hit a mine while making educated guess")
            exit(1)
    
    # Check if game is complete
    if not check_game_state():
        print("Game completed successfully!")
        break

    # Add a small delay between iterations to prevent race conditions
    time.sleep(0.1)
    print(f"Current board state({iteration}):")
    for r in range(row):
        for c in range(col):
            cell = solver.grid[r][c]
            print(f"Cell ({r}, {c}) → {cell.value if cell.value is not None else '?'}")

print("\nFinal board state:")
for r in range(row):
    for c in range(col):
        cell = solver.grid[r][c]
        print(f"Cell ({r}, {c}) → {cell.value if cell.value is not None else '?'}")
    
    

