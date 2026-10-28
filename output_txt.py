from mazegen import MazeGenerator
from custom_errors import OutputError


def _walls_to_hexa(north: bool, east: bool, south: bool, west: bool) -> str:
    value = 0
    if not north:
        value += 1
    if not east:
        value += 2
    if not south:
        value += 4
    if not west:
        value += 8
    output = format(value, "x")
    return output


def _maze_grid(maze: MazeGenerator) -> str:
    rows: list[str] = []
    for y in range(maze.height):
        row: str = ""
        for x in range(maze.width):
            row += _walls_to_hexa(maze.grid[y][x].north.is_open,
                                  maze.grid[y][x].east.is_open,
                                  maze.grid[y][x].south.is_open,
                                  maze.grid[y][x].west.is_open)
        rows.append(row)
    return "\n".join(rows)


def _full_text(maze: MazeGenerator, solution: list[str]) -> str:
    output = _maze_grid(maze)
    output += "\n\n"
    output += f"{maze.entry[0]},{maze.entry[1]}         # entry (x, y)\n"
    output += f"{maze.exit[0]},{maze.exit[1]}         # exit (x, y)\n"
    output += "".join(solution) + "\n"
    return output


def write_output(maze: MazeGenerator, filename: str, solve: list[str]) -> None:
    text = _full_text(maze, solve)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
    except OSError as e:
        raise OutputError(f"Cannot write output file "
                          f"'{filename}': {e.strerror}")


if __name__ == "__main__":
    maze = MazeGenerator(10, 15, (0, 0), (9, 14), True)
    maze.generate_maze()
    solution = maze.solve_maze()
    print(_full_text(maze, solution))
