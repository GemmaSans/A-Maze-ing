from cell_structure import Cell, WallEdge
import random


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
        if not (0 <= entry_pos[0] < width and 0 <= entry_pos[1] < height):
            raise ValueError("Entry position off limits")
        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
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
        for (x, y) in FORTY_TWO_PATTERN:
            actual_x = origin_x + x
            actual_y = origin_y + y
            self.cells[actual_x][actual_y].blocked = True

    def _get_neighbours(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Returns a list of coordinates of unvisited neighbouring
        cells of the cell in position (x, y).

        Parameters:
            x (int) = Position of the cell in the X axis, from 0 to width -1.
            y (int) = Position of the cell in the Y axis, from 0 to height -1.

        Returns:
            neighbours (list(tuple(int, int)): List of the coordinates for
            available neighbours
        """
        abs_neighbours: list[tuple[int, int]] = []
        rel_neighbours: list[tuple[int, int]] = [
            (0, -1), (1, 0), (0, 1), (-1, 0)
        ]
        for neighbour in rel_neighbours:
            abs_x = x + neighbour[0]
            abs_y = y + neighbour[1]
            if not (0 <= abs_x < self.width and 0 <= abs_y < self.height):
                continue
            if not any((self.cells[abs_x][abs_y].blocked,
                        self.cells[abs_x][abs_y].visited)):
                abs_neighbours.append((abs_x, abs_y))
        return abs_neighbours

    def _break_walls(self, current: Cell, neighbour: Cell) -> None:
        """Removes the wall shared by Cells current and neighbour"""
        dif_x = neighbour.x - current.x
        dif_y = neighbour.y - current.y
        if dif_x == 1:
            current.east.is_open = True
        elif dif_x == -1:
            current.west.is_open = True
        elif dif_y == 1:
            current.south.is_open = True
        elif dif_y == -1:
            current.north.is_open = True
        else:
            raise ValueError(f"Cells ({current.x}, {current.y}) and "
                             f"({neighbour.x}, {neighbour.y}) not adjacent")

    def _backtracking_algorithm(self) -> None:
        visited: list[Cell] = [self.cells[0][0]]
        self.cells[0][0].visited = True
        while visited:
            current: Cell = visited[-1]
            neighbours = self._get_neighbours(current.x, current.y)
            if neighbours:
                selected_coords = random.choice(neighbours)
                selected = self.cells[selected_coords[0], selected_coords[1]]
                self._break_walls(current, selected)
                selected.visited = True
                visited.append(selected)
            else:
                visited.pop()

    def generate_maze(self) -> None:
        self._build_base_grid()
        if self.has_42:
            self._block_42_cells()
        ...
