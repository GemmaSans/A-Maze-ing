from mazegen import MazeGenerator


class MazeDisplay:
    """Class for the display of the maze"""
    def __init__(self, generator: MazeGenerator,
                 path: str | None = None) -> None:
        """
        Initialization of the MazeDisplay class.

        Parameters:
            generator (MazeGenerator): the class that holds the maze data
            path (str | None): optional solution path string
            (e.g., 'ESEENE...')

        Attributes:
            show_path (bool): flag indicating if the solution path should
            be displayed.
            width_canva (int): width of the displayed maze, based in the
            original width
            height_canva (int): height of the displayed maze, based in the
            original height
            str_maze (list[list[str]]): the grid that store characters for
            display the maze in terminal
        """
        # Está por ver entre nosotras si path se pasa aparte o como parte
        # de generator
        self.generator = generator
        self.path = path
        self.show_path: bool = isinstance(self.path, str)
        self.width_canva: int = self.generator.width * 2 + 1
        self.height_canva: int = self.generator.height * 2 + 1
        self.str_maze: list[list[str]] = []

    def canva_init(self) -> None:
        """
        Creates an empty grid: 2D list of dimensions (height_canva x
        width_canva) filled with space characters (' ') and stores it in
        self.str_maze.
        """
        for y in range(self.height_canva):
            str_row: list[str] = []
            for x in range(self.width_canva):
                str_row.append(" ")
            self.str_maze.append(str_row)

    def start_exit(self) -> None:
        pass

    def str_generate(self) -> None:
        """
        Translates the integer grid into a character canvas with walls.

        Iterates over the integer matrix (using coordinates
        y, x = row, column inside the matrix), evaluates active bit flags
        (N, E, S, W) for each cell, and draws the corresponding wall 
        characters into the canvas.

        Parameters:
            int_maze (list[list[int]]): The 2D grid of bitwise wall values.
        """
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.cells[y][x]
                if x + 1 < self.generator.width:
                    next_cell = self.generator.cells[y][x + 1]
                if y + 1 < self.generator.height:
                    below_cell = self.generator.cells[y + 1][x]

                # cy = y * 2 + 1
                ny = y * 2
                sy = y * 2 + 2
                ey = y * 2 + 1
                wy = y * 2 + 1

                # cx = x * 2 + 1
                nx = x * 2 + 1
                sx = x * 2 + 1
                ex = x * 2 + 2
                wx = x * 2

                if not cell.north.is_open:
                    self.str_maze[ny][nx] = "█"
                    if next_cell and not next_cell.north.is_open:
                        self.str_maze[ny][ex] = "█"
                if not cell.south.is_open:
                    self.str_maze[sy][sx] = "█"
                    if next_cell and not next_cell.south.is_open:
                        self.str_maze[sy][ex] = "█"
                if not cell.east.is_open:
                    self.str_maze[ey][ex] = "█"
                    if not cell.north.is_open:
                        self.str_maze[ny][ex] = "█"
                    if not cell.south.is_open:
                        self.str_maze[sy][ex] = "█"
                    if below_cell and not below_cell.east.is_open:
                        self.str_maze[sy][ex] = "█"
                if not cell.west.is_open:
                    self.str_maze[wy][wx] = "█"
                    if not cell.north.is_open:
                        self.str_maze[ny][wx] = "█"
                    if not cell.south.is_open:
                        self.str_maze[sy][wx] = "█"
                    if below_cell and not below_cell.west.is_open:
                        self.str_maze[sy][wx] = "█"


def main() -> None:
    try:
        maze_structure = MazeGenerator(20, 15, (1, 1), (19, 14), False, 0)
        maze_structure.generate_maze()
        maze_to_print = MazeDisplay(maze_structure)
        maze_to_print.canva_init()
        maze_to_print.str_generate()
        for row in maze_to_print.str_maze:
            for cell in row:
                print(cell, end="")
            print()

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
