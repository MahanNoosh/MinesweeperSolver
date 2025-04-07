from PIL import Image, ImageDraw
import random

def _get_center(width, height):
    """
    Calculate the center of the image.
    
    Args:
        width (int): The width of the image.
        height (int): The height of the image.
    
    Returns:
        tuple: Coordinates (x, y) of the center.
    """
    x_center = 2 * width // 3
    y_center = 2 * height // 3
    return x_center, y_center

def _detect_tile_boundaries(image, start_x, start_y):
    """
    Detect the boundaries of a tile based on the color of the starting pixel.
    
    Args:
        image (PIL.Image): The image from which the tile boundaries will be detected.
        start_x (int): The starting x-coordinate of the tile.
        start_y (int): The starting y-coordinate of the tile.
    
    Returns:
        tuple: The bounding box of the detected tile (left, top, right, bottom).
    """
    # Get the starting color from the given coordinates
    original_color = image.getpixel((start_x, start_y))
    
    # Initialize the boundary coordinates
    top, bottom, left, right = start_y, start_y, start_x, start_x

    # Move upwards to find the top boundary
    while top > 0 and image.getpixel((start_x, top - 1)) == original_color:
        top -= 1
    
    # Move downwards to find the bottom boundary
    while bottom < image.height - 1 and image.getpixel((start_x, bottom + 1)) == original_color:
        bottom += 1
    
    # Move right to find the right boundary
    while right < image.width - 1 and image.getpixel((right + 1, start_y)) == original_color:
        right += 1
    
    # Move left to find the left boundary
    while left > 0 and image.getpixel((left - 1, start_y)) == original_color:
        left -= 1

    # Print boundaries for debugging (can be removed later)
    print(f"Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")
    
    # Check if the detected tile is valid or too close to the edges
    is_invalid_tile = (bottom - top <= 10 or right - left <= 10 or bottom - top >= 60 or right - left >= 60)
    is_out_of_bounds = (top <= 0 or bottom >= image.height or left <= 0 or right >= image.width)
    
    if is_invalid_tile or is_out_of_bounds:
        # If invalid, recursively call the function with new random coordinates
        return _detect_tile_boundaries(image, 
                                      random.randint(image.width // 4, 3 * image.width // 4), 
                                      random.randint(image.height // 4, 3 * image.height // 4))
    
    # Return the bounding box (left, top, right, bottom)
    return (left, top, right, bottom)

def _capture_tile(image, region):
    """
    Capture a tile from the image based on the given region.
    
    Args:
        image (PIL.Image): The image from which to capture the tile.
        region (tuple): The bounding box of the region (left, top, right, bottom).
    
    Returns:
        PIL.Image: The cropped tile image.
    """
    return image.crop(region)

def find_default_tiles(board_image, output_file1, output_file2):
    # Load the image
    image = Image.open("template/" + board_image)
    width, height = image.size
    
    # Calculate the center coordinates
    start_x, start_y = _get_center(width, height)
    
    # Detect the boundaries of two tiles
    region1 = _detect_tile_boundaries(image, start_x, start_y)
    region2 = _detect_tile_boundaries(image, region1[2] + 10, region1[1])  # Move 10px to the right of the first tile
    
    # Capture the tiles
    default_tile1 = _capture_tile(image, region1)
    default_tile2 = _capture_tile(image, region2)
    
    # Save the captured tiles
    if default_tile1:
        default_tile1.save("template/" + output_file1)  # Save the captured tile
    if default_tile2:
        default_tile2.save("template/" + output_file2)  # Save the captured tile
    
    gap = (region2[2] - region1[0]) // 2

    region3 = ((region1[0] + region2[0]) // 2, (region2[3] + region1[1]) // 2 - gap, (region1[2] + region2[2]) // 2, (region2[3] + region1[1]) // 2 - gap + (region2[3] - region1[1]))  # Calculate the average region for the grid sample

    grid_sample = _capture_tile(image, region3)
    grid_sample.save("template/grid_sample.png")  # Save the captured tile
    return region1, region2
