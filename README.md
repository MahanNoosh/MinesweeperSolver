# Minesweeper Solver

An automated solver for the Minesweeper game using computer vision and probabilistic reasoning.

## Features

- Automatic board detection and grid analysis
- Computer vision-based tile recognition
- Probabilistic mine detection
- Smart move selection using constraint satisfaction
- Configurable solver settings
- Detailed logging and debugging options

## Requirements

- Python 3.10 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/minesweeperSolver.git
cd minesweeperSolver
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Open your Minesweeper game
2. Run the solver:
```bash
python main.py
```

3. When prompted:
   - Move your mouse to the top-left corner of the Minesweeper board
   - Wait for 3 seconds
   - Move your mouse to the bottom-right corner of the board
   - Wait for 3 seconds
   - The solver will start automatically

## Configuration

You can modify the solver's behavior by adjusting settings in `config.py`:

- `MAX_ITERATIONS`: Maximum number of solving attempts
- `MOVE_DELAY`: Delay between moves (seconds)
- `SETUP_DELAY`: Delay during setup (seconds)
- `SIMILARITY_THRESHOLD`: Threshold for image matching
- Debug mode and other settings via `SolverConfig` class

## Project Structure

```
minesweeperSolver/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── requirements.txt     # Project dependencies
├── read/               # Image processing and board reading
│   ├── capture.py
│   ├── get_tile_number.py
│   └── ...
├── write/              # Game interaction
│   └── click.py
├── process/            # Data processing
│   └── ...
├── solver/            # Core solving logic
│   ├── __init__.py
│   └── solver_logic.py
└── template/          # Template images for matching
```

## How It Works

1. **Board Detection**: Uses computer vision to detect the Minesweeper board and grid structure
2. **Tile Recognition**: Analyzes each tile to determine its state (unopened, number, mine)
3. **Solving Strategy**:
   - Identifies safe moves using constraint satisfaction
   - Flags certain mines
   - Makes educated guesses when no certain moves are available
   - Uses probability calculations for optimal guessing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.