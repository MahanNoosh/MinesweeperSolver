from read.capture import capture_board, get_board_region, capture_tile
from read.get_starter_template import get_starter_template
from read.detect_grid_intersections_on_board import detect_grid_intersections_on_board
from read.convert_to_2d_tiles_coordinate_list import find_list_dimension, convert_to_2d_tiles_list
from write.click import click_at, initialization_click, random_click
import random
from PIL import Image

board_region = get_board_region()

capture_board("state.png", board_region)
get_starter_template("state.png", "default_tile1.png", "default_tile2.png")
intersections = detect_grid_intersections_on_board("state.png", "intersection1.png", "intersection2.png")
row, col = find_list_dimension(intersections)
grid_coordinates = convert_to_2d_tiles_list(intersections)
tile_width = grid_coordinates[0][1][0] - grid_coordinates[0][0][0]
tile_height = grid_coordinates[1][0][1] - grid_coordinates[0][0][1]
initialization_click(board_region, tile_width, tile_height)
x, y = random_click(grid_coordinates)
capture_board("state.png", board_region)
image = Image.open("template/state.png")
region = (grid_coordinates[y][x][0], grid_coordinates[y][x][1], grid_coordinates[y][x][0] + tile_width, grid_coordinates[y][x][1] + tile_height)
sc = capture_tile(image, region)
sc.save("template/captured_tile.png")
# for _ in range(100):  # Limit the loop to 100 iterations for controlled execution
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
