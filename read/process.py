from PIL import Image
import random

def get_near_center(width, height, offset=10):
    x_center = (width - 134) // 2
    y_center = (height - 134) // 2
    x_offset = random.randint(-offset, offset)
    y_offset = random.randint(-offset, offset)
    return x_center + x_offset, y_center + y_offset

def detect_color_change(image, start_x, start_y):
    original_color = image.getpixel((start_x, start_y))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    print(f"Start color: {original_color}")  # Debugging output
    
    for dx, dy in directions:
        x, y = start_x + dx, start_y + dy
        if x < 0 or y < 0 or x >= image.width or y >= image.height:
            continue  # Skip if out of bounds
        new_color = image.getpixel((x, y))
        
        print(f"Checking pixel ({x}, {y}): {new_color}")  # Debugging output
        
        if new_color != original_color:
            print(f"Color change detected at ({x}, {y})")  # Debugging output
            return (x, y)
    
    return None


def calculate_tile_dimensions(image, start_x, start_y):
    top = start_y
    bottom = start_y
    
    while top > 0 and image.getpixel((start_x, top - 1)) == image.getpixel((start_x, top)):
        top -= 1
    
    while bottom < image.height - 1 and image.getpixel((start_x, bottom + 1)) == image.getpixel((start_x, bottom)):
        bottom += 1
    
    height = bottom - top + 1
    
    left = start_x
    right = start_x
    
    while left > 0 and image.getpixel((left - 1, start_y)) == image.getpixel((left, start_y)):
        left -= 1
    
    while right < image.width - 1 and image.getpixel((right + 1, start_y)) == image.getpixel((right, start_y)):
        right += 1
    
    width = right - left + 1
    
    return width, height

def capture_tile(image, start_x, start_y, tile_width, tile_height):
    right = start_x + tile_width
    lower = start_y + tile_height

    # Ensure valid coordinates
    if right < start_x or lower < start_y:
        raise ValueError("Invalid region coordinates: right must be greater than left, and lower must be greater than upper.")
    
    region = (start_x, start_y, right, lower)
    tile_image = image.crop(region)
    return tile_image


def get_default_tile(image):
    width, height = image.size
    start_x, start_y = get_near_center(width, height)
    
    color_change_point = detect_color_change(image, start_x, start_y)
    if color_change_point:
        change_x, change_y = color_change_point
        tile_width, tile_height = calculate_tile_dimensions(image, start_x, start_y)
        return capture_tile(image, start_x, start_y, tile_width, tile_height)
    else:
        print("No color change detected.")
        return None

# Example usage
image = Image.open("template/state.png")
default_tile = get_default_tile(image)
if default_tile:
    default_tile.show()  # Display the captured tile
