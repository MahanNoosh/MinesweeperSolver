import cv2
import numpy as np

def detect_grid_on_board(board_image_path, grid_sample_image_path, threshold=0.9):
    # Load the board image (state.png)
    board_img = cv2.imread(board_image_path)
    if board_img is None:
        print(f"Error: Could not load image at {board_image_path}")
        return

    # Load the grid sample image (grid_sample.png)
    grid_sample = cv2.imread(grid_sample_image_path)
    if grid_sample is None:
        print(f"Error: Could not load image at {grid_sample_image_path}")
        return

    # Convert both images to grayscale
    board_gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
    grid_sample_gray = cv2.cvtColor(grid_sample, cv2.COLOR_BGR2GRAY)

    # Perform template matching to find all occurrences of the grid sample
    result = cv2.matchTemplate(board_gray, grid_sample_gray, cv2.TM_CCOEFF_NORMED)

    # Get the locations where the match is above the threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))  # Convert to (x, y) pairs

    # Create a copy of the original image to draw the detected grid cells
    grid_image = board_img.copy()

    # Draw rectangles around the detected grid cells
    grid_w, grid_h = grid_sample.shape[1], grid_sample.shape[0]
    for (x, y) in locations:
        cv2.rectangle(grid_image, (x, y), (x + grid_w, y + grid_h), (0, 255, 0), 2)

    # Show the image with the detected grid cells
    cv2.imshow('Detected Grid Cells', grid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
board_image_path = 'template/state.png'  # Path to the state board image
grid_sample_image_path = 'template/grid_sample.png'  # Path to the grid sample image

detect_grid_on_board(board_image_path, grid_sample_image_path)
