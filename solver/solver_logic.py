"""Core logic for solving Minesweeper puzzles."""

from typing import List, Tuple, Set, Optional
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Cell:
    """Represents a cell in the Minesweeper grid."""
    row: int
    col: int
    value: Optional[int] = None  # None = unopened, -1 = mine, 0-8 = number
    is_flagged: bool = False
    probability: float = 0.0

class SolverLogic:
    """Core logic for solving Minesweeper puzzles."""
    
    def __init__(self, rows: int, cols: int):
        """Initialize the solver logic.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.mines_found = set()
        self.safe_cells = set()
        self.total_mines = None  # Will be set based on difficulty
        
    def update_cell(self, row: int, col: int, value: int) -> None:
        """Update a cell's value in the grid.
        
        Args:
            row: Row index
            col: Column index
            value: Cell value (-1 for mine, 0-8 for numbers)
        """
        print(f"Updating SolverLogic cell at row={row}, col={col} with value={value}")
        self.grid[row][col].value = value
        if value == -1:
            self.grid[row][col].is_flagged = True
            self.mines_found.add((row, col))
    
    def get_neighbors(self, row: int, col: int) -> List[Cell]:
        """Get all valid neighboring cells.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            List of neighboring Cell objects
        """
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbors.append(self.grid[new_row][new_col])
        return neighbors
    
    def find_safe_moves(self) -> Set[Tuple[int, int]]:
        """Find cells that are definitely safe to click.
        
        Returns:
            Set of (row, col) tuples representing safe cells
        """
        safe_cells = set()
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is not None and cell.value > 0:
                    neighbors = self.get_neighbors(row, col)
                    flagged = sum(1 for n in neighbors if n.is_flagged)
                    unopened = [(n.row, n.col) for n in neighbors 
                               if n.value is None and not n.is_flagged]
                    
                    # If all mines around this cell are flagged, remaining unopened cells are safe
                    if flagged == cell.value and unopened:
                        print(f"Found safe cells around ({row}, {col}) - all mines flagged")
                        safe_cells.update(unopened)
        
        return safe_cells
    
    def find_certain_mines(self) -> Set[Tuple[int, int]]:
        """Find cells that are definitely mines.
        
        Returns:
            Set of (row, col) tuples representing mine locations
        """
        certain_mines = set()
        
        # First pass: Find obvious mines
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is not None and cell.value > 0:
                    neighbors = self.get_neighbors(row, col)
                    flagged = sum(1 for n in neighbors if n.is_flagged)
                    unopened = [(n.row, n.col) for n in neighbors 
                               if n.value is None and not n.is_flagged]
                    
                    # If number of remaining mines equals number of unopened cells
                    remaining_mines = cell.value - flagged
                    print(f"Checking cell ({row}, {col}) with value {cell.value}")
                    print(f"  Flagged neighbors: {flagged}")
                    print(f"  Unopened neighbors: {len(unopened)}")
                    print(f"  Remaining mines: {remaining_mines}")
                    
                    if remaining_mines == len(unopened) and unopened:
                        print(f"  Found {len(unopened)} certain mines around ({row}, {col})")
                        certain_mines.update(unopened)
        
        # Only return new mines that haven't been found yet
        new_mines = certain_mines - self.mines_found
        if new_mines:
            print(f"Found {len(new_mines)} new certain mines: {new_mines}")
            self.mines_found.update(new_mines)
        return new_mines
    
    def calculate_probabilities(self) -> None:
        """Calculate probability of each unopened cell being a mine."""
        # Reset probabilities
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].probability = 0.0
                
        # Calculate local constraints for each numbered cell
        constraints = []
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is not None and cell.value > 0:
                    neighbors = self.get_neighbors(row, col)
                    flagged = sum(1 for n in neighbors if n.is_flagged)
                    unopened = [(n.row, n.col) for n in neighbors 
                               if n.value is None and not n.is_flagged]
                    if unopened:
                        remaining_mines = cell.value - flagged
                        if remaining_mines >= 0:
                            # Add constraint with weight based on confidence
                            # Higher weight for more certain constraints
                            if remaining_mines == len(unopened):
                                weight = 1.0  # All unopened must be mines
                            elif remaining_mines == 0:
                                weight = 1.0  # All unopened must be safe
                            else:
                                weight = 0.5  # Less certain cases
                            constraints.append((unopened, remaining_mines, weight))
        
        # Update probabilities based on constraints
        for cells, mines, weight in constraints:
            if cells:
                prob = (mines / len(cells)) * weight
                for row, col in cells:
                    # Take the maximum probability from all constraints
                    self.grid[row][col].probability = max(self.grid[row][col].probability, prob)
                    
        # Add global mine density as a factor (reduced weight)
        total_unopened = sum(1 for r in range(self.rows) for c in range(self.cols) 
                           if self.grid[r][c].value is None and not self.grid[r][c].is_flagged)
        if total_unopened > 0:
            global_prob = len(self.mines_found) / total_unopened
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col].value is None and not self.grid[row][col].is_flagged:
                        # Blend local and global probabilities (reduced global weight)
                        self.grid[row][col].probability = (
                            0.9 * self.grid[row][col].probability + 
                            0.1 * global_prob
                        )
                        
        # Ensure no cell has probability 0 unless we're absolutely certain
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is None and not cell.is_flagged:
                    # Only set probability to 0 if all neighbors are safe
                    is_safe = True
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                                neighbor = self.grid[new_row][new_col]
                                if neighbor.value is not None and neighbor.value > 0:
                                    neighbors = self.get_neighbors(new_row, new_col)
                                    flagged = sum(1 for n in neighbors if n.is_flagged)
                                    unopened = [(n.row, n.col) for n in neighbors 
                                               if n.value is None and not n.is_flagged]
                                    if neighbor.value - flagged == len(unopened):
                                        is_safe = False
                                        break
                    if not is_safe:
                        cell.probability = max(cell.probability, 0.1)  # Minimum probability of 10%

    def make_educated_guess(self) -> set:
        """Make an educated guess about which cell to click next.
        
        Returns:
            set: A set containing the coordinates of the cell to click
        """
        min_probability = float('inf')
        best_cells = set()
        
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                # Only consider unopened cells that aren't flagged
                if cell.value is None and not cell.is_flagged:
                    if cell.probability < min_probability:
                        min_probability = cell.probability
                        best_cells = {(r, c)}
                    elif cell.probability == min_probability:
                        best_cells.add((r, c))
        
        return best_cells
     