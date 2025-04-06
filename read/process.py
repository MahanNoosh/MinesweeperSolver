from PIL import Image
import random

def get_center(width, height):
    x_center = width // 2
    y_center = height // 2
    return x_center, y_center

def detect_tile_boundaries(image, start_x, start_y):
    # Get the starting color
    original_color = image.getpixel((start_x, start_y))
    
    # Initialize boundary points
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

    # Print boundaries for debugging
    print(f"Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")
    # Check if any boundary is too close to the edges
    is_invald_tile = (
        bottom - top <= 10 or right - left <= 10
    )
    is_out_of_bounds = (
        top <= 0 or bottom >= image.height or left <= 0 or right >= image.width
    )
    
    if is_invald_tile or is_out_of_bounds:
        return detect_tile_boundaries(image, random.randint(10, image.width - 10), random.randint(10, image.height - 10))
    # Return the rectangle (left, top, right, bottom)
    return (left, top, right, bottom)

def capture_tile(image, region):
    tile_image = image.crop(region)
    return tile_image


# Example usage
image = Image.open("template/state.png")
width, height = image.size
start_x, start_y = get_center(width, height)
region = detect_tile_boundaries(image, start_x, start_y)
default_tile = capture_tile(image, region)
if default_tile:
    default_tile.save("template/default_tile.png")  # Save the captured tile
