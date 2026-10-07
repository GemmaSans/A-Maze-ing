from .wall_utils import remove_walls
from .cell_structure import Cell
import random


def _get_neighbours(x: int, y: int,
                    width: int, height: int,
                    cells: list[list[Cell]]) -> list[tuple[int, int]]:
    """
    Returns a list of coordinates of unvisited, unblocked neighbouring
    cells of the cell in position (x, y).

    Parameters:
        x (int) = Position of the cell in the X axis, from 0 to width - 1.
        y (int) = Position of the cell in the Y axis, from 0 to height - 1.
        width (int) = Total width of the maze.
        length (int) = Total length of the maze.
        cells (list(list(Cell))) = The grid of Cells from the maze

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
        if not (0 <= abs_x < width and 0 <= abs_y < height):
            continue
        if not any((cells[abs_x][abs_y].blocked,
                    cells[abs_x][abs_y].visited)):
            abs_neighbours.append((abs_x, abs_y))
    return abs_neighbours


def backtracking(width: int, height: int, cells: list[list[Cell]]) -> None:
    """
    Uses the backtracking algorithm to make the maze. Starting from
    cell at position (0, 0) it randomly chooses an available neighbour,
    breaks the wall between them, and keeps carving until if doesn't find
    any, in which case it backtracks until it can find one.
    """
    visited: list[Cell] = [cells[0][0]]
    cells[0][0].visited = True
    while visited:
        current: Cell = visited[-1]
        neighbours = _get_neighbours(current.x, current.y,
                                     width, height, cells)
        if neighbours:
            selected_coords = random.choice(neighbours)
            selected = cells[selected_coords[0]][selected_coords[1]]
            remove_walls(current, selected)
            selected.visited = True
            visited.append(selected)
        else:
            visited.pop()
