from mazegen import MazeGenerator


class MazeDisplay:
    """Class for the display of the maze"""
    def __init__(self, generator: MazeGenerator,
                 path: list[str] | None = None) -> None:
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
        self.show_path: bool = isinstance(self.path, list)
        self.width_canva: int = self.generator.width * 4 + 1
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

    def str_generate(self) -> None:
        """
        Translates the grid of Cell objects into a character canvas with walls.

        Iterates over the generator's 2D cell structure, evaluates the 
        state of the shared WallEdges (north, south, east, west) for each 
        cell, and draws the corresponding wall characters into the canvas.
        """
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.grid[y][x]
                if x - 1 <= 0:
                    prev_cell = self.generator.grid[y][x - 1]
                if y - 1 <= 0:
                    above_cell = self.generator.grid[y - 1][x]
                if x + 1 < self.generator.width:
                    next_cell = self.generator.grid[y][x + 1]
                if y + 1 < self.generator.height:
                    below_cell = self.generator.grid[y + 1][x]

                ny = y * 2
                cy = y * 2 + 1
                sy = y * 2 + 2

                wx = x * 4
                c1x = x * 4 + 1
                c2x = x * 4 + 2
                c3x = x * 4 + 3
                ex = x * 4 + 4

                if not cell.north.is_open:
                    self.str_maze[ny][c1x] = "█"
                    self.str_maze[ny][c2x] = "█"
                    self.str_maze[ny][c3x] = "█"
                    if prev_cell and not prev_cell.north.is_open:
                        self.str_maze[ny][wx] = "█"
                    if next_cell and not next_cell.north.is_open:
                        self.str_maze[ny][ex] = "█"

                if not cell.south.is_open:
                    self.str_maze[sy][c1x] = "█"
                    self.str_maze[sy][c2x] = "█"
                    self.str_maze[sy][c3x] = "█"
                    if prev_cell and not prev_cell.south.is_open:
                        self.str_maze[sy][wx] = "█"
                    if next_cell and not next_cell.south.is_open:
                        self.str_maze[sy][ex] = "█"

                if not cell.east.is_open:
                    self.str_maze[cy][ex] = "█"
                    if not cell.north.is_open:
                        self.str_maze[ny][ex] = "█"
                    if not cell.south.is_open:
                        self.str_maze[sy][ex] = "█"
                    if above_cell and not above_cell.east.is_open:
                        self.str_maze[ny][ex] = "█"
                    if below_cell and not below_cell.east.is_open:
                        self.str_maze[sy][ex] = "█"

                if not cell.west.is_open:
                    self.str_maze[cy][wx] = "█"
                    if not cell.north.is_open:
                        self.str_maze[ny][wx] = "█"
                    if not cell.south.is_open:
                        self.str_maze[sy][wx] = "█"
                    if above_cell and not above_cell.west.is_open:
                        self.str_maze[ny][wx] = "█"
                    if below_cell and not below_cell.west.is_open:
                        self.str_maze[sy][wx] = "█"

    def fill_42(self) -> None:
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.grid[y][x]
                cy = y * 2 + 1
                c1x = x * 4 + 1
                c2x = x * 4 + 2
                c3x = x * 4 + 3

                if cell.blocked:
                    self.str_maze[cy][c1x] = "▓"
                    self.str_maze[cy][c2x] = "▓"
                    self.str_maze[cy][c3x] = "▓"

    def include_entry(self) -> None:
        x, y = self.generator.entry

        cy = y * 2 + 1
        cx = x * 4 + 2

        self.str_maze[cy][cx] = "E"

    def include_exit(self) -> None:
        x, y = self.generator.exit

        cy = y * 2 + 1
        cx = x * 4 + 2

        self.str_maze[cy][cx] = "X"

    def include_path(self) -> None:
        if self.show_path:
            x, y = self.generator.entry
            for i in range(len(self.path)):
                ny = y * 2
                cy = y * 2 + 1
                sy = y * 2 + 2

                wx = x * 4
                c1x = x * 4 + 1
                c2x = x * 4 + 2
                c3x = x * 4 + 3
                ex = x * 4 + 4

                if self.path[i] == 'N':
                    self.str_maze[ny][c2x] = "┃"
                    if i < len(self.path) - 1:
                        if self.path[i + 1] == 'N':
                            self.str_maze[ny - 1][c2x] = "┃"
                        if self.path[i + 1] == 'W':
                            self.str_maze[ny - 1][c2x] = "┓"
                        if self.path[i + 1] == 'E':
                            self.str_maze[ny - 1][c2x] = "┏"
                    y -= 1
                if self.path[i] == 'S':
                    self.str_maze[sy][c2x] = "┃"
                    if i < len(self.path) - 1:
                        if self.path[i + 1] == 'S':
                            self.str_maze[sy + 1][c2x] = "┃"
                        if self.path[i + 1] == 'W':
                            self.str_maze[sy + 1][c2x] = "┛"
                        if self.path[i + 1] == 'E':
                            self.str_maze[sy + 1][c2x] = "┗"
                    y += 1
                if self.path[i] == 'W':
                    self.str_maze[cy][c1x] = "━"
                    self.str_maze[cy][wx] = "━"
                    if i < len(self.path) - 1:
                        if self.path[i + 1] == 'N':
                            self.str_maze[cy][wx - 1] = "━"
                            self.str_maze[cy][wx - 2] = "┗"
                        if self.path[i + 1] == 'S':
                            self.str_maze[cy][wx - 1] = "━"
                            self.str_maze[cy][wx - 2] = "┏"
                        if self.path[i + 1] == 'W':
                            self.str_maze[cy][wx - 1] = "━"
                            self.str_maze[cy][wx - 2] = "━"
                    x -= 1
                if self.path[i] == 'E':
                    self.str_maze[cy][c3x] = "━"
                    self.str_maze[cy][ex] = "━"
                    if i < len(self.path) - 1:
                        if self.path[i + 1] == 'N':
                            self.str_maze[cy][ex + 1] = "━"
                            self.str_maze[cy][ex + 2] = "┛"
                        if self.path[i + 1] == 'S':
                            self.str_maze[cy][ex + 1] = "━"
                            self.str_maze[cy][ex + 2] = "┓"
                        if self.path[i + 1] == 'E':
                            self.str_maze[cy][ex + 1] = "━"
                            self.str_maze[cy][ex + 2] = "━"
                    x += 1

    def choice_menu(self) -> None:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        while choice != "4":
            if choice == "1":
                print("You are generating a new maze")
                self.show_maze()
            elif choice == "2":
                if self.show_path:
                    self.show_path = False
                else:
                    self.show_path = True
                self.show_maze()
            elif choice == "3":
                print("still working on that")
                self.show_maze()
            elif choice == "4":
                print("You are quitting the maze. Good bye!")
                break

    def show_maze(self) -> None:
        self.canva_init()
        self.str_generate()
        self.include_path()
        self.include_entry()
        self.include_exit()
        self.fill_42()
        for row in self.str_maze:
            for cell in row:
                print(cell, end="")
            print()
        # print(self.path)
        self.choice_menu()


def main() -> None:
    try:
        maze_structure = MazeGenerator(20, 20, (9, 15), (19, 1), False, 0)
        maze_structure.generate_maze()
        solution = maze_structure.solve_maze()
        maze_to_print = MazeDisplay(maze_structure, solution)
        maze_to_print.show_maze()

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
