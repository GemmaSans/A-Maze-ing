from .cell_structure import Cell
import random


def _get_visitable(x: int, y: int,
                   cells: list[list[Cell]]) -> list[tuple[int, int]]:
    """
    Returns a list of coordinates of visitable neighbouring
    cells of the cell in position (x, y).

    Parameters:
        x (int) = Position of the cell in the X axis, from 0 to width - 1.
        y (int) = Position of the cell in the Y axis, from 0 to height - 1.
        cells (list(list(Cell))) = The grid of Cells from the maze.

    Returns:
        neighbours (list(tuple(int, int)): List of the coordinates for
        available neighbours
    """
    abs_neighbours: list[tuple[int, int]] = []
    current = cells[x][y]
    if current.north.is_open:
        abs_neighbours.append((x, y - 1))
    if current.east.is_open:
        abs_neighbours.append((x + 1, y))
    if current.south.is_open:
        abs_neighbours.append((x, y + 1))
    if current.west.is_open:
        abs_neighbours.append((x - 1, y))
    return abs_neighbours


def find_valid_path(cells: list[list[Cell]],
                    entry: tuple[int, int],
                    exit: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of the coordinates of the found exit.

    Parameters:
        cells (list(list(Cell))) = The grid of Cells from the maze.
        entry (tuple(int, int)) = The entry point of the maze.
        exit (tuple(int, int)) = The exit point of the maze.
    """
    trail: list[tuple[int, int]] = [entry]
    deadends: list[tuple[int, int]] = []
    while trail:
        current = trail[-1]
        visitable = _get_visitable(current[0], current[1], cells)
        for coord in visitable:
            if coord in deadends:
                visitable.remove(coord)
        if visitable:
            next_coords = random.choice(visitable)
            trail.append(next_coords)
            if next_coords == exit:
                return trail
        else:
            deadend = trail.pop()
            deadends.append(deadend)
    return trail
