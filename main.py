from read.capture import capture_board, get_board_region
from read.get_starter_template import get_starter_template
from read.detect_grid_intersections_on_board import detect_grid_intersections_on_board
from read.convert_to_2d_tiles_coordinate_list import find_list_dimension, convert_to_2d_tiles_list

board_region = get_board_region()

capture_board("state.png", board_region)
get_starter_template("state.png", "default_tile1.png", "default_tile2.png")
intersections = detect_grid_intersections_on_board("state.png", "intersection1.png", "intersection2.png")
grid_size = find_list_dimension(intersections)
grid_coordinates = convert_to_2d_tiles_list(intersections)
dx, dy = grid_coordinates[0][1][0] - grid_coordinates[0][0][0], grid_coordinates[0][0][1] - grid_coordinates[1][0][1]

# while True:
    
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
