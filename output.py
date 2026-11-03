from mazegen import MazeGenerator


class OutputError(Exception):
    """Raised when the output file cannot be created or written"""


def _walls_to_hexa(north: bool, east: bool, south: bool, west: bool) -> str:
    """
    Encodes the walls of a cell as a single lowercase hexadecimal digit.

    A closed wall sets its bit to 1 and an open wall leaves it at 0:
    north is bit 0, east bit 1, south bit 2 and west bit 3.

    Parameters:
        north (bool): True if the north wall is open.
        east (bool): True if the east wall is open.
        south (bool): True if the south wall is open.
        west (bool): True if the west wall is open.

    Returns:
        str: a single hexadecimal character, from '0' (all walls open)
        to 'f' (all walls closed).
    """
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
    """
    Builds the hexadecimal representation of the maze grid.

    Parameters:
        maze (MazeGenerator): a maze whose grid has already been generated.

    Returns:
        str: one line per row of cells, with one hex digit per cell, joined
        by newlines. The last line has no trailing newline.
    """
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


def _full_text(maze: MazeGenerator) -> str:
    """
    Builds the complete content of the output file.

    The content is the hexadecimal grid, an empty line, the entry
    coordinates, the exit coordinates and the shortest path, each on its
    own line and ending with a newline.

    Parameters:
        maze (MazeGenerator): a maze whose grid has already been generated.
        solve (list(str)): the shortest path from entry to exit, as the
            letters N, E, S and W.

    Returns:
        str: the text to write to the output file.
    """
    output = _maze_grid(maze)
    output += "\n\n"
    output += f"{maze.entry[0]},{maze.entry[1]} # entry (x, y)\n"
    output += f"{maze.exit[0]},{maze.exit[1]}   # exit (x, y)\n"
    output += "".join(maze.solution) + "\n"
    return output


def write_output(maze: MazeGenerator, filename: str) -> None:
    """
    Writes the maze to a file in the hexadecimal output format.

    Parameters:
        maze (MazeGenerator): a maze whose grid has already been generated.
        filename (str): path of the file to create or overwrite.
        solve (list(str)): the shortest path from entry to exit, as the
            letters N, E, S and W.

    Raises:
        OutputError: if the file cannot be created or written.
    """
    if not maze.grid:
        raise OutputError("The maze has not been generated yet!\n"
                          "Use the method MazeGenerator.generate_maze()"
                          " before anything else")
    text = _full_text(maze)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
    except OSError as e:
        raise OutputError(f"Cannot write output file "
                          f"'{filename}': {e.strerror}")
