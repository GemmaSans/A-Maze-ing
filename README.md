*This project has been created as part of the 42 curriculum by gsans-co, lucgomez.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python 3.10+. It reads a configuration file, generates a maze, writes it to a file using a hexadecimal wall representation, and displays it with an interactive visual representation.

The project has two parts:

- **`mazegen`**: a standalone, reusable package containing the maze generation logic (`MazeGenerator`). It knows nothing about configuration files, output formats or rendering.
- **The program** (`a_maze_ing.py`): reads the configuration, uses `mazegen` to build the maze, writes the output file and shows the maze.

### Features

- Reproducible generation through a seed.
- Two modes:
  - `PERFECT=True`: exactly one path between any two cells (no loops).
  - `PERFECT=False`: a board usable by a Pac-Man-like game. It is fully connected, has loops (several independent routes), and the four corners and the centre are open corridors. Dead-ends are removed, except the two enclosed by the "42" pattern.
- A visible "42" pattern drawn with fully closed cells. If the maze is too small to fit it (smaller than 9x7), the pattern is omitted and a message is printed.
- No open area wider than 2 cells (no fully open 3x3 block).
- Shortest path from entry to exit (breadth-first search).
- Error handling with clear messages for invalid configuration, missing files and impossible parameters.

## Instructions

### Makefile Commands

* `make` / `make all` / `make install-package`: Default target. Packages and installs `mazegen` into `maze_env`.
* `make install`: Creates the virtual environment (`maze_env`) and installs dependencies from `requirements.txt` if they have not been installed previously.
* `make build`: Packages `mazegen` into a `.whl` distribution inside `dist/` and copies the wheel file to the project root.
* `make run`: Executes `a_maze_ing.py` using `config.txt` inside the virtual environment.
* `make debug`: Launches `a_maze_ing.py config.txt` under `pdb` for interactive debugging.
* `make clean`: Removes cache directories (`__pycache__`, `.mypy_cache`).
* `make fclean`: Performs complete cleanup including removal of `dist/`, `build/`, `mazegen.egg-info`, `maze_env`, and generated output files (`maze.txt`).
* `make re`: Runs `fclean` followed by `all` to perform a full rebuild.
* `make lint`: Performs code style checks using `flake8` and static type checking with `mypy`.
* `make lint-strict`: Runs `mypy` in strict mode.

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` for linting
- `build` for packaging `mazegen` into a `.whl` distribution

Dependencies can be installed using the `make install` command.

## Installation & Execution

The repository uses a Virtual Environment (`maze_env`) managed via a standard `Makefile`. 

1. **Build and install the reusable `mazegen` package into the environment:** This produces `mazegen-*.whl` and `mazegen-*.tar.gz` in `dist/`. The built file is also kept at the root of the repository, and it could be used to install it in another project:

   ```bash
   make install-package
   ```

   *Alternatively, run with Python:*

   ```bash
   python3 -m venv maze_env
   source maze_env/bin/activate
   python3 -m build
   pip install mazegen-*.whl
   ```

2. **Run the project:**

   ```bash
   make run
   ```

   *Alternatively, run directly with Python:*

   ```bash
   ./maze_env/bin/python3 a_maze_ing.py config.txt
   ```

## Configuration file

The file contains one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored, as are blank lines. No spaces are allowed around `=`. Duplicate keys, unknown keys and missing mandatory keys are errors.

| Key | Mandatory | Description | Example |
|-----|-----------|-------------|---------|
| `WIDTH` | yes | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | yes | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | yes | Entry coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` or `False` (exact spelling) | `PERFECT=True` |
| `SEED` | no | Integer seed for reproducibility. If omitted, a random seed is chosen | `SEED=42` |

Coordinates are 0-indexed, with `(0, 0)` at the top-left. Entry and exit must be inside the maze, different from each other, and not on a cell of the "42" pattern.

Example:

```
# Default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Output file format

- One hexadecimal digit per cell, one row of cells per line.
- Each digit encodes the **closed** walls: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West. A closed wall sets its bit to 1.
- After the grid, an empty line, then three lines: the entry coordinates, the exit coordinates, and the shortest path from entry to exit using the letters `N`, `E`, `S`, `W`.
- Every line ends with `\n`.

Cells of the "42" pattern are fully closed and are written as `f`.

## Maze generation algorithm

### Perfect maze: recursive backtracker

The generator uses the **recursive backtracker** algorithm (randomised depth-first search), implemented with an explicit stack instead of recursion:

1. Start at cell `(0, 0)`, mark it visited and push it onto the stack.
2. Look at the cell on top of the stack and list its neighbours that are inside the grid, not visited and not part of the "42" pattern.
3. If there is at least one, pick one at random, open the wall between them, mark it visited and push it.
4. If there is none, pop the stack (backtrack).
5. Repeat until the stack is empty.

### Non-perfect maze: dead-end removal

When `PERFECT=False`, the perfect maze is converted into a playable board:

1. Find every dead-end (a cell with exactly one open wall).
2. For each one that is still a dead-end, shuffle its closed walls that lead to a valid neighbour (inside the grid and not part of the "42").
3. Open one of them. If this creates a fully open 3x3 block, close it again and try the next.
4. If none is possible, the dead-end is left alone. This only happens for the two cells enclosed by the "2" of the "42".

### Why this algorithm

- It is simple to implement, reason about and explain.
- It always produces a spanning tree, which is exactly a perfect maze, so the `PERFECT=True` mode needs no extra work.
- The "42" cells are handled by one extra condition when choosing neighbours.
- It produces long winding corridors, which makes large open areas unlikely.
- It is a good base for the non-perfect mode: removing dead-ends opens extra walls, which creates the loops required.
- The explicit stack avoids Python's recursion limit on large mazes.

### Shortest path

The path is found with breadth-first search, which guarantees the shortest path in an unweighted grid. The result is stored in `MazeGenerator.solution` when the maze is generated.

### The "42" pattern

The pattern is 7 cells wide and 5 tall, drawn as two 3x5 digits with a one-cell gap. It is centred in the maze with `origin = (size - pattern_size) // 2`. With this formula, the maze centre falls on the gap between the digits for odd sizes, and on a free cell for even sizes, so the centre stays an open corridor. A margin of one cell is kept around it, so the minimum maze size is 9x7.

## Reusable code

The `mazegen` package contains everything related to the maze itself:

- `MazeGenerator`: the public class.
- `Cell` and `WallEdge`: the data structures of the grid.
- The generation, dead-end removal, 3x3 checking and pathfinding logic.

The configuration parser, output writer, display and `a_maze_ing.py` are outside the package on purpose, so that a future project can reuse the generator without inheriting this program's file formats.

### Data structure

The grid is a `list[list[Cell]]` indexed as **`grid[y][x]`** (row first). Each `Cell` has `x`, `y`, `blocked`, `visited` and four wall references: `north`, `east`, `south`, `west`. Each wall is a `WallEdge` with an `is_open` attribute. A wall between two cells is **one shared object**, so both neighbouring cells always agree about it by construction.

### Usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry_pos=(0, 0),
    exit_pos=(19, 14),
    is_perfect=True,
    seed=42,
)
maze.generate_maze()
```

`seed` is optional. If it is omitted, a random seed is chosen and stored in `maze.seed`. `generate_maze()` can be called again to build a new maze.

Parameters:

| Parameter | Description |
|-----------|-------------|
| `width`, `height` | Size of the maze in cells (at least 1) |
| `entry_pos`, `exit_pos` | `(x, y)` coordinates, inside the maze, different, and not on the "42" |
| `is_perfect` | `True` for a perfect maze, `False` for a loopy maze without dead-ends |
| `seed` | Optional integer seed for reproducibility |

Invalid parameters raise `ValueError` with a descriptive message.

### Accessing the result

```python
cell = maze.grid[y][x]
cell.north.is_open     # True if the north wall is open
cell.east.is_open
cell.south.is_open
cell.west.is_open
cell.blocked           # True for cells of the "42" pattern

maze.entry             # (x, y)
maze.exit              # (x, y)
maze.solution          # shortest path from entry to exit
maze.coords_42         # coordinates of the "42" cells (empty if omitted)
```

## Visual representation

### Advanced Features & Terminal UI

The interactive display module (`display.py`) provides a terminal-based interface (`MazeDisplay`) that renders the maze in full ANSI colour —where each individual cell is scaled to $3 \times 5$ characters— alongside an interactive menu with 6 choices:

1. **Re-generate a new maze:** Dynamically creates a new maze with a random seed without restarting the application.

2. **Show / Hide shortest path:** Toggles the solution path with animated frame-by-frame rendering. The path is initially shown or hidden depending on whether the `MazeDisplay` class was instantiated with a solution path parameter.

3. **Rotate all colours:** Cycles through the ANSI colour palette across all elements simultaneously (walls, path, logo, and markers).

4. **Rotate only the 42 colours:** Rotates exclusively the ANSI colour scheme used for rendering the 42 logo pattern.

5. **Rotate only the walls colours:** Rotates exclusively the ANSI colour scheme applied to the maze walls.

6. **Quit:** Cleanly exits the interactive menu loop.

7. **42 Logo Embedding:** Automatically reserves a central region in grids $\ge 9 \times 7$ to render the "42" pattern using textured ASCII block characters (`▓`, `▒`).

## Testing

- `maze_analyzer.py`, provided with the subject, is used to check wall coherence, whether the maze is perfect or playable, and the dead-ends.

## Team and project management

### Roles

- **gsans-co**: maze generation core: data structures, "42" pattern, backtracker, non-perfect conversion, pathfinding; config parser; output file.
- **lucgomez**: display and interaction; Makefile; MazeGenerator package; README.

### Planning

The first step on the planning was to agree on the data structures for the MazeGenerator package. That way, knowing what we would end up working with, both of us could work independently without overlapping work.

### What worked well and what could be improved

- Working on separate files and branches avoided most merge conflicts.
- Agreeing early on the interface between the generator and the rest of the program.
- Writing helpers with small, single responsibilities made bugs easier to find.

### Tools used

- Python 3.10+, `flake8`, `mypy`, `build`
- Git and GitHub
- `maze_analyzer.py` (provided)

## Resources

### References

- Maze generation algorithms (recursive backtracker, Prim's, Kruskal's): https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search
- Python typing (`TypedDict`, type hints): https://docs.python.org/3/library/typing.html
- Python packaging guide: https://packaging.python.org/
- PEP 8 and PEP 257 (style and docstrings): https://peps.python.org/pep-0008/ and https://peps.python.org/pep-0257/
- TODO: add anything else you used (MiniLibX documentation, etc.)

### Use of AI

AI (Claude and Gemini) was used as a guide and reviewer, not as a code generator for the core logic. Its use was:

- Design discussion
- Concept explanations
- Code review
- Documentation

The code was written by the team, and every suggestion was reviewed, tested and understood before being kept.
