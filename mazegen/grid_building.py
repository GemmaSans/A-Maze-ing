from .cell_structure import Cell, WallEdge


FORTY_TWO_PATTERN: set[tuple[int, int]] = {
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
    (4, 0), (4, 2), (4, 3), (4, 4), (5, 0), (5, 2), (5, 4),
    (6, 0), (6, 1), (6, 2), (6, 4)
}
PATTERN_WIDTH: int = 7
PATTERN_HEIGHT: int = 5


def build_base_grid(width: int, height: int) -> list[list[Cell]]:
    """
    Generates all the needed cells and closed wall edges to have a base
    grid for the algorithm to work on.

    Parameters:
        width (int) = Total width of the maze.
        height (int) = Total height of the maze.

    Returns:
        grid (list(list(Cell))) = A grid of width x height cells
    """
    horizontal_edges = [[WallEdge() for _ in range(width)]
                        for _ in range(height + 1)]
    vertical_edges = [[WallEdge() for _ in range(width + 1)]
                      for _ in range(height)]
    grid = [[Cell(x, y,
                  north=horizontal_edges[y][x],
                  south=horizontal_edges[y + 1][x],
                  west=vertical_edges[y][x],
                  east=vertical_edges[y][x + 1])
             for x in range(width)]
            for y in range(height)]
    return grid


def _get_42_coords(width: int, height: int) -> set[tuple[int, int]]:
    """
    Obtain the absolute coordinates for the 42 logo.

    Parameters:
        width (int) = Total width of the maze.
        height (int) = Total height of the maze.

    Returns the absolute coordinates as a set(tuple(int, int))
    """
    origin_x = (width - PATTERN_WIDTH) // 2
    origin_y = (height - PATTERN_HEIGHT) // 2
    return {(origin_x + x, origin_y + y) for x, y in FORTY_TWO_PATTERN}


def _block_42_cells(grid: list[list[Cell]],
                    coords_42: set[tuple[int, int]]) -> None:
    """
    Sets the cells that will become the 42 logo as 'blocked'

    Parameters:
        grid (list(list(Cell))) = The grid of the maze
        coords_42 (set(tuple(int, int))) = The coordinates for the
            42 logo
    """
    for (x, y) in coords_42:
        grid[y][x].blocked = True
