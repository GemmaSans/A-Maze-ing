from .wall_utils import remove_walls
from .cell_structure import Cell
import random


def _get_neighbours(cell: Cell, grid: list[list[Cell]]) -> list[Cell]:
    """
    Returns a list of coordinates of unvisited, unblocked neighbouring
    cells of the cell in question.

    Parameters:
        cell (Cell): The origin cell.
        grid (list(list(Cell))): The grid of Cells that comprises the maze

    Returns:
        list(Cell)): List of available, neighbouring cells
    """
    width = len(grid[0])
    height = len(grid)
    neighbours: list[Cell] = []
    rel_neighbours: list[tuple[int, int]] = [
            (0, -1), (1, 0), (0, 1), (-1, 0)
    ]
    for neighbour in rel_neighbours:
        abs_x = cell.x + neighbour[0]
        abs_y = cell.y + neighbour[1]
        if not (0 <= abs_x < width and 0 <= abs_y < height):
            continue
        if not any((grid[abs_y][abs_x].blocked,
                    grid[abs_y][abs_x].visited)):
            neighbours.append(grid[abs_y][abs_x])
    return neighbours


def backtracking(grid: list[list[Cell]]) -> None:
    """
    Uses the backtracking algorithm to make the maze. Starting from
    cell at position (0, 0) it randomly chooses an available neighbour,
    breaks the wall between them, and keeps carving until if doesn't find
    any, in which case it backtracks until it can find one.

    Parameters:
        grid (list(list(Cell))): The grid of Cells that comprises the maze
    """
    visited: list[Cell] = [grid[0][0]]
    grid[0][0].visited = True
    while visited:
        current: Cell = visited[-1]
        neighbours = _get_neighbours(current, grid)
        if neighbours:
            selected = random.choice(neighbours)
            remove_walls(current, selected)
            selected.visited = True
            visited.append(selected)
        else:
            visited.pop()
