from read.capture import capture_board, get_board_region
from read.get_default_tiles import get_default_tile
from read.detect_grid_intersections_on_board import detect_grid_intersections_on_board

board_region = get_board_region()

capture_board("state.png", board_region)
get_default_tile("state.png", "default_tile1.png", "default_tile2.png")
intersections = detect_grid_intersections_on_board("state.png", "intersection1.png", "intersection2.png")

# while True:
    
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
