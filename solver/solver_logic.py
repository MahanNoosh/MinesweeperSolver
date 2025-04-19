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
    is_mine: bool = False
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
        self.grid[row][col].value = value
        if value == -1:
            self.grid[row][col].is_mine = True
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
                    
                    # If number of flagged neighbors equals cell value,
                    # all other neighbors are safe
                    if flagged == cell.value and unopened:
                        safe_cells.update(unopened)
        
        self.safe_cells = safe_cells                
        return safe_cells
    
    def find_certain_mines(self) -> Set[Tuple[int, int]]:
        """Find cells that are definitely mines.
        
        Returns:
            Set of (row, col) tuples representing mine locations
        """
        certain_mines = set()
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is not None and cell.value > 0:
                    neighbors = self.get_neighbors(row, col)
                    flagged = sum(1 for n in neighbors if n.is_flagged)
                    unopened = [(n.row, n.col) for n in neighbors 
                               if n.value is None and not n.is_flagged]
                    
                    # If remaining unopened cells must all be mines
                    if cell.value - flagged == len(unopened):
                        certain_mines.update(unopened)
        
        self.mines_found = certain_mines
        return certain_mines
    
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
                    unopened = [(n.row, n.col) for n in neighbors 
                               if n.value is None and not n.is_flagged]
                    if unopened:
                        flagged = sum(1 for n in neighbors if n.is_flagged)
                        remaining_mines = cell.value - flagged
                        if remaining_mines >= 0:
                            constraints.append((unopened, remaining_mines))
        
        # Update probabilities based on constraints
        for cells, mines in constraints:
            if cells:
                prob = mines / len(cells)
                for row, col in cells:
                    self.grid[row][col].probability += prob
    
    def make_educated_guess(self) -> Optional[Tuple[int, int]]:
        """Choose the best cell to click when no certain moves are available.
        
        Returns:
            Tuple of (row, col) for the chosen cell, or None if no good guess exists
        """
        self.calculate_probabilities()
        
        min_prob = float('inf')
        best_guess = None
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell.value is None and not cell.is_flagged:
                    if cell.probability < min_prob:
                        min_prob = cell.probability
                        best_guess = (row, col)
        
        self.safe_cells.add(best_guess)
        return {best_guess}
     