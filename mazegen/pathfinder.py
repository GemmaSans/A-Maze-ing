from .cell_structure import Cell
from collections import deque


def _get_visitable(x: int, y: int,
                   grid: list[list[Cell]]) -> list[tuple[int, int]]:
    """
    Returns a list of coordinates of visitable neighbouring
    cells of the cell in position (x, y).

    Parameters:
        x (int): Position of the cell in the X axis, from 0 to width - 1.
        y (int): Position of the cell in the Y axis, from 0 to height - 1.
        grid (list(list(Cell))): The grid of Cells from the maze.

    Returns:
        list(tuple(int, int): List of the coordinates for
        available neighbours
    """
    abs_neighbours: list[tuple[int, int]] = []
    current = grid[y][x]
    if current.north.is_open:
        abs_neighbours.append((x, y - 1))
    if current.east.is_open:
        abs_neighbours.append((x + 1, y))
    if current.south.is_open:
        abs_neighbours.append((x, y + 1))
    if current.west.is_open:
        abs_neighbours.append((x - 1, y))
    return abs_neighbours


def _coord_to_cardinals(solution: list[tuple[int, int]]) -> list[str]:
    """
    Converts a list of coordinates to a list of cardinal directions.

    Parameters:
        solution (list[tuple[int, int]]): A list of coordinates

    Returns:
        list[str]: A list of the solution in cardinal directions.
    """
    solution_list: list[str] = []
    for i in range(0, len(solution) - 1):
        current = solution[i]
        next = solution[i + 1]
        diff_x = next[0] - current[0]
        diff_y = next[1] - current[1]
        if diff_x == 1:
            solution_list.append("E")
        elif diff_x == -1:
            solution_list.append("W")
        elif diff_y == 1:
            solution_list.append("S")
        elif diff_y == -1:
            solution_list.append("N")
    return solution_list


def bfs(grid: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int]) -> list[str]:
    """
    Uses Breadth-First Search (BFS) to obtain the shortest path
    from a point to the other.

    Parameters:
        grid (list(list(Cell))): The grid of Cells that comprises the maze
        entry (tuple[int, int]): The entry point of the maze.
        exit (tuple[int, int]): The exit point of the maze.

    Returns:
        list(str): A list of the shortest path in cardinal directions.
    """
    queue = deque([exit])
    visited = {exit}
    next: dict[tuple[int, int], tuple[int, int]] = {}
    while queue:
        current = queue.popleft()
        visitable = _get_visitable(current[0], current[1], grid)
        visitable = [coord for coord in visitable if coord not in visited]
        for cell in visitable:
            visited.add(cell)
            next[cell] = current
            if cell == entry:
                queue.clear()
                break
            queue.append(cell)
    solution = [entry]
    current = entry
    while current != exit:
        current = next[current]
        solution.append(current)
    return _coord_to_cardinals(solution)
