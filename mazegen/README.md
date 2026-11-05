# mazegen

A small, dependency-free Python library that generates mazes. It was written for the 42 project *A-Maze-ing*, but it knows nothing about configuration files, output formats or rendering, so it can be reused in any other project.

## Features

- Reproducible generation through a seed.
- **Perfect mazes**: exactly one path between any two cells (no loops).
- **Loopy mazes**: fully connected, with several independent routes, the four corners and the centre open, and no dead-ends (except the two enclosed by the "42" pattern).
- A "42" pattern drawn with fully closed cells (omitted if the maze is too small).
- No fully open 3x3 area anywhere.
- Shortest path from entry to exit, computed when the maze is generated.

Requires Python 3.10 or later. No third-party dependencies.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

To build it from the sources:

```bash
python3 -m venv venv
source venv/bin/activate
pip install build
python3 -m build
```

The files are created in `dist/`.

## Quick start

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

print(maze.solution)
```

`generate_maze()` must be called before reading `grid` or `solution`. Until then they are empty.

## Parameters

```python
MazeGenerator(width, height, entry_pos, exit_pos, is_perfect=False, seed=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns, at least 1 |
| `height` | `int` | Number of rows, at least 1 |
| `entry_pos` | `tuple[int, int]` | Entry cell `(x, y)` |
| `exit_pos` | `tuple[int, int]` | Exit cell `(x, y)` |
| `is_perfect` | `bool` | `True` for a perfect maze, `False` for a maze with loops and no dead-ends (default) |
| `seed` | `int \| None` | Seed for reproducibility. If omitted, a random seed is chosen |

Coordinates are 0-indexed, with `(0, 0)` at the top-left. `x` grows to the right and `y` grows downwards.

The entry and exit must be inside the maze, must be different, and must not be on a cell of the "42" pattern. Otherwise a `ValueError` with a descriptive message is raised.

### Seeds

The same parameters and the same seed always give the same maze. The seed used is stored in `maze.seed`, including when it is chosen randomly, so an interesting maze can be reproduced later.

```python
a = MazeGenerator(20, 15, (0, 0), (19, 14), seed=7)
b = MazeGenerator(20, 15, (0, 0), (19, 14), seed=7)
a.generate_maze()
b.generate_maze()
# a and b contain identical mazes
```

### Regenerating

`generate_maze()` rebuilds the maze from scratch each time. Calling it again with the same seed gives the same maze. To get a different one, change the seed first:

```python
import random

maze.seed = random.randrange(2**32)
maze.generate_maze()
```

## Accessing the maze

### The grid

`maze.grid` is a `list[list[Cell]]` indexed **row first**: `maze.grid[y][x]`.

Each `Cell` has:

| Attribute | Description |
|-----------|-------------|
| `x`, `y` | Position of the cell |
| `north`, `east`, `south`, `west` | The four walls of the cell |
| `blocked` | `True` for cells of the "42" pattern |

Each wall is a `WallEdge` with an `is_open` attribute (`True` if you can walk through it). A wall between two neighbouring cells is **one shared object**, so both cells always agree about it:

```python
cell = maze.grid[2][3]          # x=3, y=2
cell.east.is_open               # True if the wall to the east is open
cell.east is maze.grid[2][4].west   # True: same wall object
```

Outer walls (the border of the maze) are always closed. Cells of the "42" pattern have all four walls closed.

### Other attributes

| Attribute | Description |
|-----------|-------------|
| `maze.width`, `maze.height` | Size of the maze |
| `maze.entry`, `maze.exit` | Entry and exit positions `(x, y)` |
| `maze.is_perfect` | The mode that was requested |
| `maze.seed` | The seed in use |
| `maze.coords_42` | Set of `(x, y)` cells that form the "42". Empty if the pattern does not fit |
| `maze.solution` | The shortest path from entry to exit as a list of `"N"`, `"E"`, `"S"`, `"W"` letters |

### The "42" pattern

The pattern is 7 cells wide and 5 tall and is centred in the maze, with a margin of one cell. The smallest maze that can contain it is 9x7. For anything smaller, `maze.coords_42` is empty and no pattern is drawn. The library does not print anything in that case, so check `maze.coords_42` if you need to warn the user.

### Example: reading the walls

```python
for row in maze.grid:
    line = ""
    for cell in row:
        line += "#" if cell.blocked else "."
    print(line)
```

### Example: using the solution

```python
maze = MazeGenerator(12, 12, (0, 0), (11, 11), seed=1)
maze.generate_maze()
steps = len(maze.solution)
print(f"The shortest path has {steps} steps")
```

## Algorithms

- **Generation**: recursive backtracker (randomised depth-first search) with an explicit stack, so large mazes do not hit Python's recursion limit. It always produces a perfect maze.
- **Loopy mode**: after the perfect maze is built, every dead-end gets one extra wall opened towards a neighbouring cell, unless that would create a fully open 3x3 area. The cells enclosed by the "42" cannot be fixed and remain as dead-ends.
- **Solving**: breadth-first search, which gives the shortest path.

## Errors

| Exception | When |
|-----------|------|
| `ValueError` | Invalid size, entry or exit (out of bounds, equal, or on the "42" pattern) |

## License

See `LICENSE.md` at the root of the repository.
