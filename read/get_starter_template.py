from PIL import Image, ImageDraw
from read.capture import capture_tile
from collections import deque
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
    if not (image.width // 3 <= start_x <= 2 * image.width // 3 and image.height // 3 <= start_y <= 2 * image.height // 3):
        return None
    
    original_color = image.getpixel((start_x, start_y))

    top, bottom = start_y, start_y
    left, right = start_x, start_x

    while top > 0 and color_similar(image.getpixel((start_x, top - 1)), original_color):
        top -= 1
    while bottom < image.height - 1 and color_similar(image.getpixel((start_x, bottom + 1)), original_color):
        bottom += 1
    while right < image.width - 1 and color_similar(image.getpixel((right + 1, start_y)), original_color):
        right += 1
    while left > 0 and color_similar(image.getpixel((left - 1, start_y)), original_color):
        left -= 1

    print(f"Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")
    width = right - left + 1
    height = bottom - top + 1
    print(width / height, height / width)
    
    is_invalid_tile = (
        right - left == 0 or bottom - top == 0 or
        width / height > 1.2 or
        height / width > 1.2
    )
    is_out_of_bounds = (
        top <= 0 or bottom >= image.height or
        left <= 0 or right >= image.width
    )

    if is_invalid_tile or is_out_of_bounds:
        return None

    return (left, top, right, bottom)


def _detect_tile_boundaries(image, start_x = None, start_y = None):
    """
    Always detect the boundaries of a tile based on the color of the starting pixel.

    Args:
        image (PIL.Image): The image to analyze.
        start_x (int): The starting x-coordinate.
        start_y (int): The starting y-coordinate.

    Returns:
        tuple: The bounding box of the detected tile (left, top, right, bottom).

    Raises:
        ValueError: If no tile is found (e.g. image is empty or contains no tiles).
    """
    if start_x and start_y:
        tile = _detect_tile_boundaries_helper(image, start_x, start_y)
        if tile:
            return tile
    else:
        for x in range(image.width // 3, 2 * image.width // 3):
            for y in range(image.height // 3, 2 * image.height // 3):
                tile = _detect_tile_boundaries_helper(image, x, y)
                if tile:
                    return tile
    raise ValueError("No tile found")

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

    region1 = _detect_tile_boundaries(image)
    x_offset = 2 * (region1[2] - region1[0]) // 3
    region2 = _detect_tile_boundaries(image, region1[2] + x_offset, (region1[1] + region1[3]) // 2)

    default_tile1 = capture_tile(image, region1)
    default_tile2 = capture_tile(image, region2)

    if default_tile1:
        default_tile1.save("template/" + output_file1)
    if default_tile2:
        default_tile2.save("template/" + output_file2)

    get_intersection(image, region1, region2, "intersection1.png", "intersection2.png")
