import cv2

def find_list_dimension(intersections, tolerance=3):
    """
    Estimate grid dimensions based on consistent Y values in the first row.
    """
    first_row_y = intersections[0][1]
    col = 0
    for point in intersections:
        if abs(point[1] - first_row_y) > tolerance:
            break
        col += 1

    row = len(intersections) // col
    return row + 1, col + 1


def convert_to_2d_tiles_list(intersections):
    """
    Convert a flat list of intersections into a 2D grid of tile corner coordinates,
    including synthetic borders (top row and left/right columns).
    """
    row, col = find_list_dimension(intersections)
    width = intersections[1][0] - intersections[0][0]
    height = intersections[col][1] - intersections[0][1]

    all_tiles_coordinates = []

    for i in range(row - 1):
        row_start_index = i * (col - 1)
        core_row = intersections[row_start_index : row_start_index + col - 1]
        extended_row = [(core_row[0][0] - width, core_row[0][1])] + core_row
        all_tiles_coordinates.append(extended_row)

    # Prepend synthetic top row
    top_row = [(x, y - height) for x, y in all_tiles_coordinates[0]]
    all_tiles_coordinates.insert(0, top_row)

    # Optionally draw for debug
    # _draw_grid_points("template/state.png", all_tiles_coordinates)
    return all_tiles_coordinates  # 2D list [row][col] of (x, y)


def _draw_grid_points(image_path, grid_points, output_path="debug_grid.png"):
    """
    Draw red dots on the given image at each grid point and save the result.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return

    for row in grid_points:
        for (x, y) in row:
            cv2.circle(img, (int(x), int(y)), radius=3, color=(0, 0, 255), thickness=-1)

    for (x, y) in grid_points[0]:
            cv2.circle(img, (int(x), int(y)), radius=3, color=(0, 255, 0), thickness=-1)

    
    cv2.imshow("Grid Visualization", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
