from .cell_structure import Cell


def count_open_walls(cell: Cell) -> int:
    """
    Counts how many walls a given cell has.

    Parameters:
        cell: a Cell object to check

    Returns:
        The number of closed walls around the cell.
    """
    walls = (cell.north, cell.east, cell.south, cell.west)
    return sum(wall.is_open for wall in walls)


def _is_3x3_open(ori_x: int, ori_y: int, grid: list[list[Cell]]) -> bool:
    """
    Checks whether there is a 3x3 open space in the maze in the given position.

    Parameters:
        origin_x: leftmost coordinate of the area to check.
        origin_y: topmost coordinate of the area to check.
        grid: the grid of Cells that comprises the maze.

    Returns:
        True if there exists a 3x3 open area in the given coordinates,
        False otherwise.
    """
    height = len(grid)
    width = len(grid[0])
    if any((ori_y < 0, ori_x < 0, ori_y + 3 > height, ori_x + 3 > width)):
        return False
    for y in range(3):
        for x in range(2):
            if not grid[ori_y + y][ori_x + x].east.is_open:
                return False
    for x in range(3):
        for y in range(2):
            if not grid[ori_y + y][ori_x + x].south.is_open:
                return False
    return True


def creates_3x3(x1: int, y1: int, x2: int, y2: int,
                grid: list[list[Cell]]) -> bool:
    """
    Checks whether breaking a wall between two cells has generated a 3x3
    open space.

    Parameters:
        x1: Coordinate x of cell1
        y1: Coordinate y of cell1
        x2: Coordinate x of cell2
        y2: Coordinate y of cell2
        grid: the grid of Cells that comprises the maze.

    Returns:
        True if it has generated a 3x3 open space, False otherwise.
    """
    diff_x = x2 - x1
    diff_y = y2 - y1
    if abs(diff_x) + abs(diff_y) != 1:
        raise ValueError("Cells are not adjacent")
    if not diff_x:
        top = min(y1, y2)
        for x in range(x1 - 2, x1 + 1):
            for y in range(top - 1, top + 1):
                if _is_3x3_open(x, y, grid):
                    return True
    elif not diff_y:
        left = min(x1, x2)
        for x in range(left - 1, left + 1):
            for y in range(y1 - 2, y1 + 1):
                if _is_3x3_open(x, y, grid):
                    return True
    return False
