from .cell_structure import Cell


def is_3x3_open(origin_x: int, origin_y: int, cells: list[list[Cell]]) -> bool:
    """
    Checks whether there is a 3x3 open space in the maze in the given position.

    Parameters:
        origin_x: leftmost coordinate of the area to check.
        origin_y: topmost coordinate of the area to check.
        cells: the grid of Cells that comprises the maze.

    Returns:
        True if there exists a 3x3 open area in the given coordinates,
        False otherwise.
    """
    height = len(cells)
    width = len(cells[0])
    if any((origin_y < 0, origin_x < 0, origin_y + 3 > height,
            origin_x + 3 > width)):
        return False
    for y in range(3):
        for x in range(2):
            wall_status = cells[origin_y + y][origin_x + x].east.is_open
            if not wall_status:
                return False
    for x in range(3):
        for y in range(2):
            wall_status = cells[origin_y + y][origin_x + x].south.is_open
            if not wall_status:
                return False
    return True
