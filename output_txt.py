from mazegen import MazeGenerator


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


if __name__ == "__main__":
    maze = MazeGenerator(10, 15, (0, 0), (9, 14), True, 4)
    maze.generate_maze()
    print(_maze_grid(maze))
