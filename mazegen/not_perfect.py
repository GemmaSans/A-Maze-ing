from .maze_validation import count_open_walls
from .cell_structure import Cell


def obtain_deadends(grid: list[list[Cell]]) -> list[Cell]:
    deadend_list: list[Cell] = []
    for row in grid:
        for cell in row:
            if count_open_walls(cell) == 1:
                deadend_list.append(cell)
    return deadend_list
