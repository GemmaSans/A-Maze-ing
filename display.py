from mazegen import MazeGenerator


int_maze: list[list[int]] = [
    [9, 1, 3, 9, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5,
     1, 5, 5, 1, 5, 3, 9, 5, 1, 5, 3],
    [10, 12, 2, 10, 9, 1, 0, 2, 8, 2, 9, 1, 1,
     3, 8, 5, 5, 6, 9, 2, 12, 3, 10, 9, 2],
    [8, 1, 4, 4, 0, 2, 10, 10, 12, 4, 2, 10, 12,
     2, 10, 9, 1, 3, 8, 4, 5, 2, 10, 8, 6],
    [10, 8, 1, 1, 6, 10, 10, 8, 5, 5, 2, 8, 1, 2,
     12, 0, 0, 2, 8, 1, 3, 8, 6, 8, 3],
    [8, 6, 8, 6, 9, 6, 8, 4, 5, 1, 4, 2, 10, 8, 3,
     8, 6, 8, 4, 6, 12, 6, 9, 4, 2],
    [8, 1, 2, 9, 4, 1, 4, 3, 9, 4, 3, 10, 8, 2, 8,
     4, 5, 2, 9, 5, 5, 3, 8, 1, 2],
    [8, 4, 4, 6, 9, 4, 3, 10, 8, 5, 2, 12, 2, 12,
     4, 5, 1, 2, 10, 9, 5, 2, 8, 6, 10],
    [10, 9, 5, 1, 2, 9, 2, 12, 2, 15, 8, 1, 6, 15,
     15, 10, 10, 12, 2, 9, 6, 8, 5, 2],
    [8, 4, 1, 6, 12, 2, 8, 5, 2, 15, 12, 4, 1, 5,
     7, 15, 8, 2, 9, 2, 8, 5, 4, 5, 2],
    [8, 1, 4, 5, 3, 10, 12, 5, 6, 15, 15, 15, 10,
     15, 15, 8, 6, 10, 10, 8, 1, 5, 3, 10],
    [8, 4, 1, 1, 2, 8, 1, 3, 9, 1, 3, 15, 10, 15,
     13, 5, 0, 3, 12, 2, 10, 12, 1, 0, 2],
    [8, 1, 2, 10, 8, 2, 10, 12, 6, 12, 2, 15, 10,
     15, 15, 15, 10, 12, 5, 4, 6, 9, 2, 10, 10],
    [10, 10, 10, 10, 10, 8, 4, 5, 3, 9, 4, 3, 12,
     1, 1, 1, 4, 1, 3, 9, 5, 6, 10, 10, 10],
    [8, 6, 8, 2, 12, 4, 5, 3, 12, 4, 3, 12, 3, 12,
     6, 12, 3, 10, 8, 2, 9, 1, 6, 12, 2],
    [8, 3, 10, 12, 1, 1, 1, 4, 5, 1, 6, 9, 2, 9, 1,
     5, 2, 8, 6, 10, 8, 6, 9, 5, 6],
    [8, 2, 12, 3, 8, 6, 8, 1, 5, 4, 1, 6, 12, 4, 2,
     9, 2, 10, 9, 6, 8, 5, 6, 9, 3],
    [8, 2, 9, 4, 2, 9, 6, 8, 1, 1, 4, 1, 1, 3, 8, 4,
     4, 4, 2, 9, 4, 5, 5, 2, 10],
    [10, 12, 6, 9, 4, 4, 3, 10, 10, 8, 3, 10, 10, 8,
     4, 1, 3, 9, 2, 12, 3, 9, 3, 8, 2],
    [8, 3, 9, 4, 5, 3, 10, 8, 2, 12, 4, 6, 8, 4, 5,
     6, 8, 2, 8, 1, 2, 10, 10, 8, 2],
    [12, 4, 4, 5, 5, 6, 12, 6, 12, 5, 5, 5, 4, 5, 5,
     5, 4, 6, 12, 4, 4, 6, 12, 4, 6]
]


class MazeDisplay:
    """Class for the display of the maze"""
    def __init__(self, generator: MazeGenerator,
                 path: str | None = None) -> None:
        """
        Initialization of the MazeDisplay class.

        Parameters:
            generator (MazeGenerator): the class that holds the maze data
            path (str | None): optional solution path string (e.g., 'ESEENE...')

        Attributes:
            show_path (bool): flag indicating if the solution path should be displayed.
            width_canva (int): width of the displayed maze, based in the original width
            height_canva (int): height of the displayed maze, based in the original height
            str_maze (list[list[str]]): the grid that store characters for display the maze in terminal
        """
        # Está por ver entre nosotras si path se pasa aparte o como parte de generator
        self.generator = generator
        self.path = path
        self.show_path: bool = isinstance(self.path, str)
        self.width_canva: int = self.generator.width * 2 + 1
        self.height_canva: int = self.generator.height * 2 + 1
        self.str_maze: list[list[str]] = []

    def canva_init(self) -> None:
        """
        Creates an empty grid: 2D list of dimensions (height_canva x width_canva) filled 
        with space characters (' ') and stores it in self.str_maze.
        """
        for row in range(self.height_canva):
            str_row: list[str] = []
            for cell in range(self.width_canva):
                str_row.append(" ")
            self.str_maze.append(str_row)
        for x in range(0, self.width_canva):
            self.str_maze[0][x] = "█"
        for x in range(0, self.width_canva):
            self.str_maze[self.height_canva - 1][x] = "█"
        for y in range(0, self.height_canva):
            self.str_maze[y][0] = "█"
        for y in range(0, self.height_canva):
            self.str_maze[y][self.width_canva - 1] = "█"

    def str_maze_generator(self, int_maze: list[list[int]]) -> None:
        """
        Translates the integer grid into a character canvas with walls.

        Iterates over the integer matrix (using coordinates
        y, x = row, column inside the matrix), evaluates active bit flags
        (N, E, S, W) for each cell, and draws the corresponding wall 
        characters into the canvas.

        Parameters:
            int_maze (list[list[int]]): The 2D grid of bitwise wall values.
        """
        for y, row in enumerate(int_maze):
            for x, cell in enumerate(row):
                # cy = y * 2 + 1 █ _ | ¯
                ny = y * 2
                sy = y * 2 + 2
                ey = y * 2 + 1
                wy = y * 2 + 1
                # cx = x * 2 + 1
                nx = x * 2 + 1
                sx = x * 2 + 1
                ex = x * 2 + 2
                wx = x * 2

                n_wall = cell & 1
                s_wall = cell & 4
                e_wall = cell & 2
                w_wall = cell & 8

                if n_wall:
                    self.str_maze[ny][nx] = "█"
                if s_wall:
                    self.str_maze[sy][sx] = "█"
                if e_wall:
                    self.str_maze[ey][ex] = "█"
                if w_wall:
                    self.str_maze[wy][wx] = "█"


def main() -> None:
    maze_structure = MazeGenerator(25, 20, (1, 1), (19, 14), False, 0)
    maze = MazeDisplay(maze_structure)
    maze.canva_init()
    maze.str_maze_generator(int_maze)
    for row in maze.str_maze:
        for cell in row:
            print(cell, end="")
        print()


if __name__ == "__main__":
    main()
