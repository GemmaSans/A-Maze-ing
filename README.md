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

### Installation & Execution

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

## Advanced Features & Terminal UI

The interactive display module (`display.py`) provides a terminal-based interface (`MazeDisplay`) that renders the maze in full ANSI colour —where each individual cell is scaled to $3 \times 5$ characters— alongside an interactive menu with 6 choices:

1. **Re-generate a new maze:** Dynamically creates a new maze with a random seed without restarting the application.

2. **Show / Hide shortest path:** Toggles the solution path with animated frame-by-frame rendering. The path is initially shown or hidden depending on whether the `MazeDisplay` class was instantiated with a solution path parameter.

3. **Rotate all colours:** Cycles through the ANSI colour palette across all elements simultaneously (walls, path, logo, and markers).

4. **Rotate only the 42 colours:** Rotates exclusively the ANSI colour scheme used for rendering the 42 logo pattern.

5. **Rotate only the walls colours:** Rotates exclusively the ANSI colour scheme applied to the maze walls.

6. **Quit:** Cleanly exits the interactive menu loop.

7. **42 Logo Embedding:** Automatically reserves a central region in grids $\ge 9 \times 7$ to render the "42" pattern using textured ASCII block characters (`▓`, `▒`).