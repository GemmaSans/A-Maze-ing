from .cell_structure import Cell
from .wall_utils import create_walls, remove_walls
import random


def _is_3x3_open(ori_x: int, ori_y: int, grid: list[list[Cell]]) -> bool:
    """
    Checks whether there is a 3x3 open space in the maze in the given position.

    Parameters:
        ori_x: leftmost coordinate of the area to check.
        ori_y: topmost coordinate of the area to check.
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


def creates_3x3(cell1: Cell, cell2: Cell, grid: list[list[Cell]]) -> bool:
    """
    Checks whether breaking a wall between two cells has generated a 3x3
    open space.

    Parameters:
        cell1: one of the cells involved.
        cell2: the other cell involved.
        grid: the grid of Cells that comprises the maze.

    Returns:
        True if it has generated a 3x3 open space, False otherwise.
    """
    diff_x = cell2.x - cell1.x
    diff_y = cell2.y - cell1.y
    if abs(diff_x) + abs(diff_y) != 1:
        raise ValueError("Cells are not adjacent")
    if not diff_x:
        top = min(cell1.y, cell2.y)
        for x in range(cell1.x - 2, cell1.x + 1):
            for y in range(top - 1, top + 1):
                if _is_3x3_open(x, y, grid):
                    return True
    elif not diff_y:
        left = min(cell1.x, cell2.x)
        for x in range(left - 1, left + 1):
            for y in range(cell1.y - 2, cell1.y + 1):
                if _is_3x3_open(x, y, grid):
                    return True
    return False


def _count_open_walls(cell: Cell) -> int:
    """
    Counts how many walls a given cell has open around it.

    Parameters:
        cell: a Cell object to check

    Returns:
        The number of open walls around the cell.
    """
    walls = (cell.north, cell.east, cell.south, cell.west)
    return sum(wall.is_open for wall in walls)


def _obtain_deadends(grid: list[list[Cell]]) -> list[Cell]:
    deadend_list: list[Cell] = []
    for row in grid:
        for cell in row:
            if _count_open_walls(cell) == 1:
                deadend_list.append(cell)
    return deadend_list


def _get_deadend_neighbours(cell: Cell, grid: list[list[Cell]]) -> list[Cell]:
    width = len(grid[0])
    height = len(grid)
    neighbours: list[Cell] = []
    directions = [(0, -1, cell.north), (1, 0, cell.east),
                  (0, 1, cell.south), (-1, 0, cell.west)]
    for x, y, edge in directions:
        abs_x = cell.x + x
        abs_y = cell.y + y
        if edge.is_open:
            continue
        if not (0 <= abs_x < width and 0 <= abs_y < height):
            continue
        if not grid[abs_y][abs_x].blocked:
            neighbours.append(grid[abs_y][abs_x])
    return neighbours


def convert_to_imperfect(grid: list[list[Cell]]) -> None:
    deadend_list = _obtain_deadends(grid)
    for current in deadend_list:
        if _count_open_walls(current) != 1:
            continue
        candidates = _get_deadend_neighbours(current, grid)
        random.shuffle(candidates)
        for neighbour in candidates:
            remove_walls(current, neighbour)
            if creates_3x3(current, neighbour, grid):
                create_walls(current, neighbour)
            else:
                break
