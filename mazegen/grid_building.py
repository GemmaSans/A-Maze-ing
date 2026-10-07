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
    """
    horizontal_edges = [[WallEdge() for _ in range(height + 1)]
                        for _ in range(width)]
    vertical_edges = [[WallEdge() for _ in range(height)]
                      for _ in range(width + 1)]
    cells = [[Cell(x, y,
                   north=horizontal_edges[x][y],
                   south=horizontal_edges[x][y + 1],
                   west=vertical_edges[x][y],
                   east=vertical_edges[x + 1][y])
              for y in range(height)]
             for x in range(width)]
    return cells


def _get_42_cells(width: int, height: int) -> set[tuple[int, int]]:
    """Returns the absolute coordinates for the 42 logo"""
    origin_x = (width - PATTERN_WIDTH) // 2
    origin_y = (height - PATTERN_HEIGHT) // 2
    return {(origin_x + x, origin_y + y) for x, y in FORTY_TWO_PATTERN}


def _block_42_cells(cells: list[list[Cell]],
                    coords_42: set[tuple[int, int]]) -> None:
    """Sets the cells that will become the 42 logo as 'blocked'"""
    for (x, y) in coords_42:
        cells[x][y].blocked = True
