tile_width = 0
tile_height = 0

def initialize_tile_dimensions(width, height):
    """
    Initialize the tile dimensions.
    
    Args:
        width (int): The width of a tile.
        height (int): The height of a tile.
    """
    global tile_width, tile_height
    tile_width = width
    tile_height = height

def get_tile_region(row, col, grid_coordinates):
    """
    Get the region of a tile in the grid.
    
    Args:
        row (int): The row index of the tile.
        col (int): The column index of the tile.
        grid_coordinates (list): The coordinates of each tile in the grid.
    
    Returns:
        tuple: The region of the tile (left, top, right, bottom).
    """
    left = grid_coordinates[row][col][0]
    top = grid_coordinates[row][col][1]
    right = left + tile_width
    bottom = top + tile_height
    return left, top, right, bottom

def get_all_tile_regions(grid_coordinates):
    """
    Get the regions of all tiles in the grid.
    
    Args:
        grid_coordinates (list): The coordinates of each tile in the grid.
    
    Returns:
        list: A list of regions for each tile in the grid.
    """
    return [[get_tile_region(row, col, grid_coordinates) for row in range(len(grid_coordinates))] for col in range(len(grid_coordinates[0]))]
    