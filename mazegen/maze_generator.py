from .grid_building import get_42_coords, build_base_grid, block_42_cells
from .algorithm_backtrack import backtracking
from .pathfinder import bfs
from .not_perfect import convert_to_imperfect
from .cell_structure import Cell
import random


PATTERN_MIN_WIDTH: int = 9
PATTERN_MIN_HEIGHT: int = 7
MAX_WIDTH: int = 200
MAX_HEIGHT: int = 200


class MazeGenerator():
    """Class for the generation of mazes"""
    def __init__(self,
                 width: int,
                 height: int,
                 entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int],
                 is_perfect: bool | None = False,
                 seed: int | None = None) -> None:
        """
        Initialization of the MazeGenerator class.

        Parameters:
            width (int): width of the maze
            height (int): height of the maze
            entry_pos (tuple(int, int)): position of the entry of the maze
            exit_pos (tuple(int, int)): position of the exit of the maze
            is_perfect (bool): True if the maze is perfect, False otherwise.
                Default is True.
            seed (int): seed for reproducibility. If none is provided, a
                random one is generated
        """
        if width < 1:
            raise ValueError("Width needs to be larger")
        if width > MAX_WIDTH:
            raise ValueError(f"Width cannot be larger than {MAX_WIDTH}")
        if height < 1:
            raise ValueError("Height needs to be larger")
        if height > MAX_HEIGHT:
            raise ValueError(f"Height cannot be larger than {MAX_HEIGHT}")

        self.width = width
        self.height = height
        self.is_perfect = is_perfect
        if seed is None:
            seed = random.randrange(2**32)
        self.seed = seed
        self.coords_42: set[tuple[int, int]] = set()

        if not (0 <= entry_pos[0] < width and 0 <= entry_pos[1] < height):
            raise ValueError("Entry position off limits")
        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError("Exit position off limits")
        if width >= PATTERN_MIN_WIDTH and height >= PATTERN_MIN_HEIGHT:
            self.coords_42 = get_42_coords(self.width, self.height)
            if entry_pos in self.coords_42:
                raise ValueError("Entry position in 42 pattern")
            if exit_pos in self.coords_42:
                raise ValueError("Exit position in 42 pattern")
        if exit_pos == entry_pos:
            raise ValueError("Entry and exit on same cell")

        self.entry = entry_pos
        self.exit = exit_pos
        self.grid: list[list[Cell]] = []
        self.solution: list[str] = []
        if not self.coords_42:
            print("[WARNING] Maze is too small to contain the 42 pattern")

    def _build_grid(self) -> None:
        """
        Generates the grid and stores it, while also blocking the 42 pattern
        """
        self.grid = build_base_grid(self.width, self.height)
        if len(self.coords_42):
            block_42_cells(self.grid, self.coords_42)

    def _backtracking_algorithm(self) -> None:
        """Uses the backtracking algorithm to break walls between cells."""
        backtracking(self.grid)

    def _solve_maze(self) -> None:
        """Saves the solution of the maze in a parameter"""
        self.solution = bfs(self.grid, self.entry, self.exit)

    def generate_maze(self, seed: int | None = None) -> None:
        """Generates the maze using a backtracking algorithm."""
        if seed:
            self.seed = seed
        random.seed(self.seed)
        self._build_grid()
        self._backtracking_algorithm()
        if not self.is_perfect:
            convert_to_imperfect(self.grid)
        self._solve_maze()
