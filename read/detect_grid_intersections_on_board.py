import cv2
import numpy as np

def detect_grid_intersections_on_board(board_image, intersection1_image, intersection2_image, threshold=0.98):
    """
    Detects grid intersection points on a board image using template matching with two sample intersection images.

    Args:
        board_image (str): Filename of the board image (e.g., "state.png").
        intersection1_image (str): Filename of the first intersection sample image.
        intersection2_image (str): Filename of the second intersection sample image.
        threshold (float): Matching confidence threshold (default is 0.98).

    Returns:
        list of tuple: List of unique (x, y) positions for detected grid intersections.
    """
    # Load the board image
    board_img = cv2.imread("template/" + board_image)
    if board_img is None:
        print(f"Error: Could not load image at template/{board_image}")
        return

    # Load intersection sample images
    grid_sample1 = cv2.imread("template/" + intersection1_image)
    grid_sample2 = cv2.imread("template/" + intersection2_image)
    if grid_sample1 is None or grid_sample2 is None:
        print("Error: Could not load one or both intersection templates.")
        return

    # Convert images to grayscale
    board_gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
    sample1_gray = cv2.cvtColor(grid_sample1, cv2.COLOR_BGR2GRAY)
    sample2_gray = cv2.cvtColor(grid_sample2, cv2.COLOR_BGR2GRAY)

    # Perform template matching for both samples
    matches = []
    result1 = cv2.matchTemplate(board_gray, sample1_gray, cv2.TM_CCOEFF_NORMED)
    result2 = cv2.matchTemplate(board_gray, sample2_gray, cv2.TM_CCOEFF_NORMED)
    locs1 = np.where(result1 >= threshold)
    locs2 = np.where(result2 >= threshold)
    sample_matches1 = list(zip(*locs1[::-1]))
    sample_matches2 = list(zip(*locs2[::-1]))

    # Alternate between the two sets of matches
    max_len = max(len(sample_matches1), len(sample_matches2))
    for i in range(max_len):
        if i < len(sample_matches1):
            matches.append(sample_matches1[i])
        if i < len(sample_matches2):
            matches.append(sample_matches2[i])

    # Deduplicate nearby points (within dist_thresh)
    def deduplicate(points, dist_thresh=5):
        unique = []
        for pt in points:
            if all(np.linalg.norm(np.array(pt) - np.array(u)) > dist_thresh for u in unique):
                unique.append(pt)
        return unique

    matches = deduplicate(matches)

    # Draw circles at detected points (for debugging / visualization)
    grid_image = board_img.copy()
    grid_w, grid_h = grid_sample1.shape[1], grid_sample1.shape[0]
    for i in range(len(matches)):
        x, y = matches[i]
        matches[i] = (x + grid_w // 2, y + grid_h // 2)
        cv2.circle(grid_image, matches[i], 3, (0, 255, 0), -1)
        
    # Uncomment below lines to preview detected matches
    # cv2.imshow('Detected Grid Intersections', grid_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return matches
