from read.capture import capture_board, get_board_region, capture_tile
from read.get_starter_template import get_starter_template
from read.detect_grid_intersections_on_board import detect_grid_intersections_on_board
from process.convert_to_2d_tiles_coordinate_list import find_list_dimension, convert_to_2d_tiles_list
from write.click import click_at, initialization_click, random_click
from read.get_tile_number import get_tile_number
from read.get_tile_region import get_tile_region, initialize_tile_dimensions
from process.update_around_empty_tile import update_around_empty_tile
from PIL import Image
import os
import time


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

grid = [[None for _ in range(col)] for _ in range(row)]

initialization_click(board_region, tile_width, tile_height)
r_row, r_col = random_click(grid_coordinates)
# everything above should stay as is below this are things that can be wrapped to a function

time.sleep(1)

capture_board("state.png", board_region)
image = Image.open("template/state.png")
region = (get_tile_region(r_row, r_col, grid_coordinates))
sc = capture_tile(image, region)
number = get_tile_number(sc)
grid[r_row][r_col] = number if number else 0
if grid[r_row][r_col] == 0:
    update_around_empty_tile(r_row, r_col, grid, grid_coordinates)
print(grid)


# for _ in range(100):  # Limit the loop to 100 iterations for controlled execution
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
