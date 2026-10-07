from .cell_structure import Cell


def _break_walls(cell1: Cell, cell2: Cell) -> None:
    """
    Removes the wall shared by two cells entered as parameter.

    Parameters:
        cell1 (Cell) = First cell.
        cell2 (Cell) = Second cell.
    """
    diff_x = cell2.x - cell1.x
    diff_y = cell2.y - cell1.y
    if diff_x == 1:
        cell1.east.is_open = True
    elif diff_x == -1:
        cell1.west.is_open = True
    elif diff_y == 1:
        cell1.south.is_open = True
    elif diff_y == -1:
        cell1.north.is_open = True
    else:
        raise ValueError(f"Cells ({cell1.x}, {cell1.y}) and "
                         f"({cell2.x}, {cell2.y}) not adjacent")
