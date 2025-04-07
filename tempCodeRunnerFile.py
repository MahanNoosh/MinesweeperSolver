from read.capture import capture_board, get_board_region
from read.find_default_tiles import find_default_tiles

board_region = get_board_region()

capture_board("state.png", board_region)
find_default_tiles("state.png", "default_tile1.png", "default_tile2.png")

# while True:
    
    # update_internal_board()
    # make_moves()
    # click_safe_tiles()
    # flag_mines()
    # if no_certain_moves:
    #     guess_or_use_ability()
