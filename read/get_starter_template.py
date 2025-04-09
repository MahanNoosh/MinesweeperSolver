from PIL import Image, ImageDraw
from read.capture import capture_tile
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
    original_color = image.getpixel((start_x, start_y))

    top, bottom = start_y, start_y
    left, right = start_x, start_x

    while top > 0 and image.getpixel((start_x, top - 1)) == original_color:
        top -= 1
    while bottom < image.height - 1 and image.getpixel((start_x, bottom + 1)) == original_color:
        bottom += 1
    while right < image.width - 1 and image.getpixel((right + 1, start_y)) == original_color:
        right += 1
    while left > 0 and image.getpixel((left - 1, start_y)) == original_color:
        left -= 1

    print(f"Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")

    is_invalid_tile = (
        bottom - top <= 10 or right - left <= 10 or
        bottom - top >= 60 or right - left >= 60
    )
    is_out_of_bounds = (
        top <= 0 or bottom >= image.height or
        left <= 0 or right >= image.width
    )

    if is_invalid_tile or is_out_of_bounds:
        return _detect_tile_boundaries(
            image,
            random.randint(image.width // 4, 3 * image.width // 4),
            random.randint(image.height // 4, 3 * image.height // 4)
        )

    return (left, top, right, bottom)

def get_intersection(image, region1, region2, output_file1, output_file2):
    """
    Capture cross-like adjacent intersection tiles between region1 and region2.
    """
    gap = region2[0] - region1[2]
    
    region3 = (
        (region1[0] + region2[0]) // 2,
        (region2[3] + region1[1]) // 2 + gap // 2,
        (region1[2] + region2[2]) // 2,
        (region2[3] + region1[1]) // 2 + gap // 2 + (region2[3] - region1[1])
    )
    
    height = region3[3] - region3[1]
    
    region4 = (
        region3[0],
        region3[1] + height + gap,
        region3[2],
        region3[3] + height + gap
    )
    
    grid_sample1 = capture_tile(image, region3)
    grid_sample2 = capture_tile(image, region4)
    
    grid_sample1.save("template/" + output_file1)
    grid_sample2.save("template/" + output_file2)

    # Debug: visualize the regions on the original image
    # debug_img = image.copy()
    # draw = ImageDraw.Draw(debug_img)
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
    width, height = image.size

    start_x, start_y = _get_center(width, height)

    region1 = _detect_tile_boundaries(image, start_x, start_y)
    region2 = _detect_tile_boundaries(image, region1[2] + 10, region1[1])

    default_tile1 = capture_tile(image, region1)
    default_tile2 = capture_tile(image, region2)

    if default_tile1:
        default_tile1.save("template/" + output_file1)
    if default_tile2:
        default_tile2.save("template/" + output_file2)

    get_intersection(image, region1, region2, "intersection1.png", "intersection2.png")
