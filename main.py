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
initialization_click(board_region, tile_width, tile_height)
r_row, r_col = random_click(grid_coordinates)
# everything above should stay as is below this are things that can be wrapped to a function
time.sleep(1)
solver = SolverLogic(row, col)
no_good = True
while no_good:
    r_row, r_col = random_click(grid_coordinates)  
    capture_board("state.png", board_region)
    image = Image.open("template/state.png")
    region = (get_tile_region(r_row, r_col, grid_coordinates))
    sc = capture_tile(image, region)
    number = get_tile_number(sc)
    solver.grid[r_row][r_col].value = int(number) if number else 0
    if solver.grid[r_row][r_col].value == 0:
        update_around_empty_tile(r_row, r_col, solver.grid, grid_coordinates)
        no_good = False
if all([all([cell.value == 0 for cell in row]) for row in solver.grid]):
    print("The board is unreadable. Please zoom in and try again.")
    exit(0)




for _ in range(100):  # Limit the loop to 100 iterations for controlled execution
    s = solver.find_safe_moves()
    print(s)
    for row, col in s:
        click_at(grid_coordinates[row][col][0], grid_coordinates[row][col][1])
    click_all(s)
    m = solver.find_certain_mines()
    for row, col in m:
        click_at(grid_coordinates[row][col][0], grid_coordinates[row][col][1])
    print(m)
    # flag_all(m)
    e = solver.make_educated_guess()
    for row, col in e:
        click_at(grid_coordinates[row][col][0], grid_coordinates[row][col][1])
    print(e)
    # click_all(e)
    capture_board("state.png", board_region)
    image = Image.open("template/state.png")
    tiles = get_all_tile_regions(grid_coordinates)
    new_grid = read_board_numbers(image, tiles)
    for r in range(row):
        for c in range(col):
            if new_grid[r][c]:
                solver.update_cell(r, c, new_grid[r][c])
    
    

