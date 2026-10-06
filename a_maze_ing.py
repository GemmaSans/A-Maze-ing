from cell_structure import Cell, WallEdge


PATTERN_WIDTH: int = 7
PATTERN_HEIGHT: int = 5
FORTY_TWO_PATTERN: set[tuple[int, int]] = {
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
    (4, 0), (4, 2), (4, 3), (4, 4), (5, 0), (5, 2), (5, 4),
    (6, 0), (6, 1), (6, 2), (6, 4)
}


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
        if exit_pos == entry_pos:
            raise ValueError("Entry and exit on same cell")
        if any((entry_pos[0] < 0, entry_pos[0] >= width,
               entry_pos[1] < 0, entry_pos[1] >= height)):
            raise ValueError("Entry position off limits")
        if any((exit_pos[0] < 0, exit_pos[0] >= width,
               exit_pos[1] < 0, exit_pos[1] >= height)):
            raise ValueError("Exit position off limits")

        self.width = width
        self.height = height
        self.entry = entry_pos
        self.exit = exit_pos
        self.is_perfect = is_perfect
        self.seed = seed
        if width < PATTERN_WIDTH + 2 or height < PATTERN_HEIGHT + 2:
            self.has_42 = False
        else:
            self.has_42 = True

    def _build_base_grid(self) -> None:
        """
        Generates all the cells and closed wall edges to have a grid for
        the algorithm to work on.
        """
        horizontal_edges = [[WallEdge() for _ in range(self.height + 1)]
                            for _ in range(self.width)]
        vertical_edges = [[WallEdge() for _ in range(self.height)]
                          for _ in range(self.width + 1)]
        cells = [[Cell(x, y,
                       north=horizontal_edges[x][y],
                       south=horizontal_edges[x][y + 1],
                       west=vertical_edges[x][y],
                       east=vertical_edges[x + 1][y])
                  for y in range(self.height)]
                 for x in range(self.width)]
        self.horizontal_edges = horizontal_edges
        self.vertical_edges = vertical_edges
        self.cells = cells

    def _block_42_cells(self) -> None:
        """Blocks the cells that will become the 42 logo"""
        origin_x = (self.width - PATTERN_WIDTH) // 2
        origin_y = (self.height - PATTERN_HEIGHT) // 2
        self.blocked_cells: set[tuple[int, int]] = set()
        for (x, y) in FORTY_TWO_PATTERN:
            actual_x = origin_x + x
            actual_y = origin_y + y
            self.blocked_cells.add((actual_x, actual_y))

    def generate_maze(self) -> None:
        self._build_base_grid()
        if self.has_42:
            self._draw_42_pattern()
        ...
