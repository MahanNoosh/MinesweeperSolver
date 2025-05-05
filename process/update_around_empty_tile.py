from collections import deque
from read.get_tile_number import get_tile_number
from read.capture import capture_tile

def update_around_empty_tile(i_row, i_col, solver, board_img, tile_regions):
    """
    Perform BFS starting from an already-known empty tile.
    Only blank tiles ('') are enqueued. Numbered tiles are updated but not enqueued.
    """

    def is_within_bounds(r, c):
        return 0 <= r < len(solver.grid) and 0 <= c < len(solver.grid[0])

    def read_and_update(r, c):
        if solver.grid[r][c].value is not None:
            return None  # already processed

        try:
            tile_img = capture_tile(board_img, tile_regions[r][c])
            number = get_tile_number(tile_img)
            if number == '':
                solver.update_cell(r, c, 0)
                return ''
            elif number.isdigit():
                solver.update_cell(r, c, int(number))
                return number
        except Exception as e:
            print(f"Error reading tile at ({r}, {c}): {e}")
        return None

    visited = set()
    queue = deque()

    # Start BFS from neighbors of the known-empty tile
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = i_row + dr, i_col + dc
            if not is_within_bounds(nr, nc):
                continue

            result = read_and_update(nr, nc)
            if result is not None:
                visited.add((nr, nc))
                if result == '':
                    queue.append((nr, nc))

    # Continue BFS on all revealed empty tiles
    while queue:
        row, col = queue.popleft()

        # Explore neighbors of this empty tile
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if not is_within_bounds(nr, nc) or (nr, nc) in visited:
                    continue

                result = read_and_update(nr, nc)
                if result is not None:
                    visited.add((nr, nc))
                    if result == '':
                        queue.append((nr, nc))
