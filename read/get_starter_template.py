from PIL import Image, ImageDraw
from read.capture import capture_tile
from collections import deque
import random

def color_similar(c1, c2, threshold=15):
    return sum(abs(a - b) for a, b in zip(c1, c2)) < threshold


def _detect_tile_boundaries_helper(image, start_x, start_y):
    """
    Detect the boundaries of a tile based on the color of the starting pixel.
    
    Args:
        image (PIL.Image): The image from which the tile boundaries will be detected.
        start_x (int): The starting x-coordinate of the tile.
        start_y (int): The starting y-coordinate of the tile.
    
    Returns:
        tuple: The bounding box of the detected tile (left, top, right, bottom).
    """
    # Add padding to avoid edge detection issues
    padding = 5
    if not (padding <= start_x <= image.width - padding and padding <= start_y <= image.height - padding):
        return None
    
    original_color = image.getpixel((start_x, start_y))

    top, bottom = start_y, start_y
    left, right = start_x, start_x

    # Find boundaries with more conservative color matching
    while top > padding and color_similar(image.getpixel((start_x, top - 1)), original_color, threshold=10):
        top -= 1
    while bottom < image.height - padding and color_similar(image.getpixel((start_x, bottom + 1)), original_color, threshold=10):
        bottom += 1
    while right < image.width - padding and color_similar(image.getpixel((right + 1, start_y)), original_color, threshold=10):
        right += 1
    while left > padding and color_similar(image.getpixel((left - 1, start_y)), original_color, threshold=10):
        left -= 1

    width = right - left + 1
    height = bottom - top + 1
    
    # More lenient aspect ratio check
    is_invalid_tile = (
        right - left == 0 or bottom - top == 0 or
        width / height > 1.5 or
        height / width > 1.5
    )
    is_out_of_bounds = (
        top <= padding or bottom >= image.height - padding or
        left <= padding or right >= image.width - padding
    )

    if is_invalid_tile or is_out_of_bounds:
        return None

    return (left, top, right, bottom)


def _detect_tile_boundaries(image, start_x = None, start_y = None):
    """
    Detect the boundaries of a tile based on the color of the starting pixel.

    Args:
        image (PIL.Image): The image to analyze.
        start_x (int): The starting x-coordinate.
        start_y (int): The starting y-coordinate.

    Returns:
        tuple: The bounding box of the detected tile (left, top, right, bottom).

    Raises:
        ValueError: If no tile is found (e.g. image is empty or contains no tiles).
    """
    # Convert image to RGB if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get image dimensions
    width, height = image.size
    
    # If no starting point provided, try multiple points
    if start_x is None or start_y is None:
        # Try center points first
        start_x = width // 2
        start_y = height // 2
        tile = _detect_tile_boundaries_helper(image, start_x, start_y)
        if tile:
            return tile
            
        # If center fails, try a grid pattern
        step = 5  # Reduced step size for more thorough search
        for x in range(width // 4, 3 * width // 4, step):
            for y in range(height // 4, 3 * height // 4, step):
                tile = _detect_tile_boundaries_helper(image, x, y)
                if tile:
                    return tile
    else:
        # Try the provided starting point
        tile = _detect_tile_boundaries_helper(image, start_x, start_y)
        if tile:
            return tile
            
        # If provided point fails, try nearby points
        for dx in range(-5, 6, 5):
            for dy in range(-5, 6, 5):
                if dx == 0 and dy == 0:
                    continue
                new_x = start_x + dx
                new_y = start_y + dy
                if 0 <= new_x < width and 0 <= new_y < height:
                    tile = _detect_tile_boundaries_helper(image, new_x, new_y)
                    if tile:
                        return tile
    
    raise ValueError("No tile found - please ensure the board is properly captured and visible")

def get_intersection(image, region1, region2, output_file1, output_file2):
    """
    Capture cross-like adjacent intersection tiles between region1 and region2.
    """
    gap = region2[0] - region1[2]
    
    region3 = (
        (region1[0] + region2[0]) // 2,
        (region2[3] + region1[1]) // 2 + gap // 2 + 1,
        (region1[2] + region2[2]) // 2,
        (region2[3] + region1[1]) // 2 + gap // 2 + (region2[3] - region1[1]) + 1
    )
    
    height = region3[3] - region3[1]
    
    region4 = (
        region3[0],
        region3[1] + height + gap + 1,
        region3[2],
        region3[3] + height + gap + 1
    )
    
    grid_sample1 = capture_tile(image, region3)
    grid_sample2 = capture_tile(image, region4)
    
    grid_sample1.save("template/" + output_file1)
    grid_sample2.save("template/" + output_file2)

    # Debug: visualize the regions on the original image
    # debug_img = image.copy()
    # draw = ImageDraw.Draw(debug_img)
    # draw.rectangle(region1, outline="green")
    # draw.rectangle(region2, outline="yellow")
    # draw.rectangle(region3, outline="red")
    # draw.rectangle(region4, outline="blue")
    # debug_img.show()

def get_starter_template(board_image, output_file1, output_file2):
    """
    Detect and save two default tiles and their intersection areas.
    
    Args:
        board_image (str): Filename of the board image inside the 'template' folder.
        output_file1 (str): Filename to save the first tile.
        output_file2 (str): Filename to save the second tile.
    """
    image = Image.open("template/" + board_image)

    # Find first tile
    region1 = _detect_tile_boundaries(image)
    if not region1:
        raise ValueError("Could not find first tile")
    
    # Calculate tile dimensions
    tile_width = region1[2] - region1[0]
    tile_height = region1[3] - region1[1]
    
    # Try to find second tile directly to the right of first tile
    # Start slightly inside the second tile to avoid edge detection issues
    start_x = region1[2] + tile_width // 2
    start_y = region1[1] + tile_height // 2
    
    # If that fails, try a few pixels to the right
    for offset in [0, 2, -2, 4, -4]:
        try:
            region2 = _detect_tile_boundaries(image, start_x + offset, start_y)
            if region2:
                # Verify this is actually the next tile to the right
                if region2[0] > region1[2]:  # Second tile starts after first tile ends
                    break
                # If not, try again
                region2 = None
        except ValueError:
            continue
    
    if not region2:
        raise ValueError("Could not find second tile next to first tile")
    
    # Save the tiles
    default_tile1 = capture_tile(image, region1)
    default_tile2 = capture_tile(image, region2)

    if default_tile1:
        default_tile1.save("template/" + output_file1)
    if default_tile2:
        default_tile2.save("template/" + output_file2)

    # Get intersection patterns
    get_intersection(image, region1, region2, "intersection1.png", "intersection2.png")
