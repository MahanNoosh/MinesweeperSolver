from read.capture import capture_tile
from read.get_tile_number import get_tile_number

def read_board_numbers(board_image, tiles_region): 
    board = [[None for _ in range(len(tiles_region[0]))] for _ in range(len(tiles_region))]
    for row in range(len(tiles_region)):
        for col in range(len(tiles_region[0])):
            number = get_tile_number(capture_tile(board_image, tiles_region[row][col]))
            board[row][col] = int(number) if number else None
    return board
        
        
        