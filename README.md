# MinesweeperSolver

An automated Minesweeper solver combining computer vision and probabilistic reasoning to make smart moves with minimal input.

---

##  Why I Built It

I developed MinesweeperSolver to explore combining **real-time vision**, **logic inference**, and **automation**. It allowed me to practice computer vision techniques, constraint solving, and system design in Python.

---

##  Features

- **Board Detection** – Detects game grid and tile states via computer vision.  
- **Tile Recognition** – Differentiates safe, numbered, and hidden tiles.  
- **Smart Solver** – Uses constraint logic and probability to guide moves.  
- **Flexible Configuration** – Customize settings like delays or move strategies via `config.py`.  
- **Detailed Logging** – Trace solver decisions and game progress.

---

##  Installation & Usage

```bash
git clone https://github.com/MahanNoosh/MinesweeperSolver.git
cd MinesweeperSolver
pip install -r requirements.txt
python main.py
```
## How It Works
1. Detect the board using CV
2. Read current tile states
3. Apply logic and probability to evaluate moves
4. Execute moves and repeat until solved or forced to guess
   
## Professional Highlights
- Applied computer vision techniques for dynamic game detection
- Designed a constraint-based solver with probabilistic fallback logic
- Built a configurable and testable system with clean logging and structure

---

## ⚠️ Limitations & How You Can Help

Right now, the solver only works reliably on **Google Minesweeper**.  
This is because Google’s version uses standard text-based numbers, which the solver can easily detect.  

Other Minesweeper versions often use **custom graphics or unusual fonts**, making it harder for the solver to read the board.  

💡 **How you can help**:  
- Improve the image recognition so it works on Minesweepers with graphical numbers.  
- Add support for multiple themes and resolutions.  
- Share screenshots or examples of Minesweeper boards where the solver fails.  

If you’re interested in fixing this, feel free to open an [issue](https://github.com/MahanNoosh/MinesweeperSolver/issues) or contribute a pull request! 
