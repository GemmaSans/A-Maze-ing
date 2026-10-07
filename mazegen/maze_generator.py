from . import grid_building
from .algorithm_backtrack import backtracking


PATTERN_WIDTH: int = 7
PATTERN_HEIGHT: int = 5
PATTERN_ALLOWANCE: int = 2


class MazeGenerator():
    """Class for the generation of mazes"""
    def __init__(self,
                 width: int,
                 height: int,
                 entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int],
                 is_perfect: bool,
                 seed: int) -> None:
        """
        Initialization of the MazeGenerator class.

        Parameters:
            width (int): width of the maze
            height (int): height of the maze
            entry_pos (tuple(int, int)): position of the entry of the maze
            exit_pos (tuple(int, int)): position of the exit of the maze
            is_perfect (bool): True if the maze is perfect, False otherwise
            seed (int): seed for reproducibility
        """
        if width < 1:
            raise ValueError("Width needs to be larger")
        if height < 1:
            raise ValueError("Height needs to be larger")

        self.width = width
        self.height = height
        self.is_perfect = is_perfect
        self.seed = seed

        if not (0 <= entry_pos[0] < width and 0 <= entry_pos[1] < height):
            raise ValueError("Entry position off limits")
        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError("Exit position off limits")
        if (width < PATTERN_WIDTH + PATTERN_ALLOWANCE or
                height < PATTERN_HEIGHT + PATTERN_ALLOWANCE):
            self.has_42 = False
        else:
            self.has_42 = True
        if self.has_42:
            self.coords_42 = grid_building._get_42_cells(self.width,
                                                         self.height)
            if entry_pos in self.coords_42:
                raise ValueError("Entry position in 42 pattern")
            if exit_pos in self.coords_42:
                raise ValueError("Exit position in 42 pattern")
        if exit_pos == entry_pos:
            raise ValueError("Entry and exit on same cell")

        self.entry = entry_pos
        self.exit = exit_pos

    def _build_base_grid(self) -> None:
        """
        Generates the grid and stores it, while also blocking the 42 pattern
        """
        self.cells = grid_building.build_base_grid(self.width, self.height)
        if self.has_42:
            grid_building._block_42_cells(self.cells, self.coords_42)

    def _backtracking_algorithm(self) -> None:
        backtracking(self.width, self.height, self.cells)

    def generate_maze(self) -> None:
        """Generates the maze using a backtracking algorithm."""
        self._build_base_grid()
        self._backtracking_algorithm()
