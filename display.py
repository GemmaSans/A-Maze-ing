from mazegen import MazeGenerator
import random
import os
import subprocess


class MazeDisplay:
    """Class for the display of the maze"""
    def __init__(self, generator: MazeGenerator,
                 path: list[str] | None = None) -> None:
        """
        Initialization of the MazeDisplay class.

        Parameters:
            generator (MazeGenerator): the class that holds the maze data
            path (list[str] | None): optional solution path sequence
            (e.g., ['E', 'S', 'E', ...])

        Attributes:
            show_path (bool): flag indicating if the solution path should
            be displayed.
            width_canva (int): width of the displayed maze, based on the
            original width.
            height_canva (int): height of the displayed maze, based on the
            original height.
            str_maze (list[list[str]]): the grid that stores characters for
            displaying the maze in the terminal.
            colours (dict[str, str]): dictionary mapping color names to their
            respective ANSI escape codes.
            colour_index (int): internal index tracker for dynamic color
            rotation.
        """

        self.generator = generator
        self.path = path
        self.show_path: bool = isinstance(self.path, list)
        self.width_canva: int = self.generator.width * 4 + 1
        self.height_canva: int = self.generator.height * 2 + 1
        self.str_maze: list[list[str]] = []
        self.colours: dict[str, str] = {"red": "\033[31m",
                                        "green": "\033[32m",
                                        "yellow": "\033[38;2;255;230;0m",
                                        "blue": "\033[34m",
                                        "magenta": "\033[35m",
                                        "cyan": "\033[36m",
                                        "white": "\033[37m"
                                        }
        self.colour_index: int = 0

    def canva_init(self) -> None:
        """
        Creates an empty grid: 2D list of dimensions (height_canva x
        width_canva) filled with space characters (' ') and stores it in
        self.str_maze.
        """
        self.str_maze = []

        for y in range(self.height_canva):
            str_row: list[str] = []
            for x in range(self.width_canva):
                str_row.append(" ")
            self.str_maze.append(str_row)

    def str_generate(self) -> None:
        """
        Translates the grid of Cell objects into a character canvas with walls.

        Iterates over the generator's 2D cell structure, safely evaluates
        adjacent neighbors (prev, above, next, below), checks whether each
        cell's walls are open or closed, and draws the corresponding wall
        characters into the canvas only if the wall is closed.
        """
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.grid[y][x]
                prev_cell = None
                above_cell = None
                next_cell = None
                below_cell = None
                if x - 1 >= 0:
                    prev_cell = self.generator.grid[y][x - 1]
                if x + 1 < self.generator.width:
                    next_cell = self.generator.grid[y][x + 1]
                if y - 1 >= 0:
                    above_cell = self.generator.grid[y - 1][x]
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
                    if above_cell and not above_cell.west.is_open:
                        self.str_maze[ny][wx] = "█"
                    if above_cell and not above_cell.east.is_open:
                        self.str_maze[ny][ex] = "█"

                if not cell.south.is_open:
                    self.str_maze[sy][c1x] = "█"
                    self.str_maze[sy][c2x] = "█"
                    self.str_maze[sy][c3x] = "█"
                    if prev_cell and not prev_cell.south.is_open:
                        self.str_maze[sy][wx] = "█"
                    if next_cell and not next_cell.south.is_open:
                        self.str_maze[sy][ex] = "█"
                    if below_cell and not below_cell.west.is_open:
                        self.str_maze[sy][wx] = "█"
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

    def fill_42(self) -> None:
        """
        Fills specific inner cells with '▓' characters to render the '42'
        logo pattern inside the maze canvas based on blocked cells.
        """
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.grid[y][x]
                prev_cell = None
                above_cell = None
                next_cell = None
                below_cell = None
                if x - 1 >= 0:
                    prev_cell = self.generator.grid[y][x - 1]
                if x + 1 < self.generator.width:
                    next_cell = self.generator.grid[y][x + 1]
                if y - 1 >= 0:
                    above_cell = self.generator.grid[y - 1][x]
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

                if cell.blocked:
                    self.str_maze[cy][c1x] = "▒"
                    self.str_maze[cy][c2x] = "▒"
                    self.str_maze[cy][c3x] = "▒"
                    if prev_cell and prev_cell.blocked:
                        self.str_maze[cy][wx] = "▒"
                    else:
                        self.str_maze[ny][wx] = "▓"
                        self.str_maze[cy][wx] = "▓"
                        self.str_maze[sy][wx] = "▓"
                    if next_cell and next_cell.blocked:
                        self.str_maze[cy][ex] = "▒"
                    else:
                        self.str_maze[ny][ex] = "▓"
                        self.str_maze[cy][ex] = "▓"
                        self.str_maze[sy][ex] = "▓"
                    if above_cell and above_cell.blocked:
                        self.str_maze[ny][c1x] = "▒"
                        self.str_maze[ny][c2x] = "▒"
                        self.str_maze[ny][c3x] = "▒"
                    else:
                        self.str_maze[ny][ex] = "▓"
                        self.str_maze[ny][c1x] = "▓"
                        self.str_maze[ny][c2x] = "▓"
                        self.str_maze[ny][c3x] = "▓"
                        self.str_maze[ny][wx] = "▓"
                    if below_cell and below_cell.blocked:
                        self.str_maze[sy][c1x] = "▒"
                        self.str_maze[sy][c2x] = "▒"
                        self.str_maze[sy][c3x] = "▒"
                    else:
                        self.str_maze[sy][ex] = "▓"
                        self.str_maze[sy][c1x] = "▓"
                        self.str_maze[sy][c2x] = "▓"
                        self.str_maze[sy][c3x] = "▓"
                        self.str_maze[sy][wx] = "▓"

    def include_entry(self) -> None:
        """
        Places the entry point marker ('E') on the maze canvas
        using the generator's entry coordinates.
        """
        x, y = self.generator.entry

        cy = y * 2 + 1
        cx = x * 4 + 2

        self.str_maze[cy][cx] = "E"

    def include_exit(self) -> None:
        """
        Places the exit point marker ('X') on the maze canvas
        using the generator's exit coordinates.
        """
        x, y = self.generator.exit

        cy = y * 2 + 1
        cx = x * 4 + 2

        self.str_maze[cy][cx] = "X"

    def include_path(self) -> None:
        """
        Calculates and draws the solution path using directional characters
        ('┃', '━', '┓', etc.) onto the canvas grid.
        """
        x, y = self.generator.entry
        solution = self.generator.solve_maze()
        for i in range(len(solution)):
            ny = y * 2
            cy = y * 2 + 1
            sy = y * 2 + 2

            wx = x * 4
            c1x = x * 4 + 1
            c2x = x * 4 + 2
            c3x = x * 4 + 3
            ex = x * 4 + 4

            if solution[i] == 'N':
                self.str_maze[ny][c2x] = "┃"
                if i < len(solution) - 1:
                    if solution[i + 1] == 'N':
                        self.str_maze[ny - 1][c2x] = "┃"
                    elif solution[i + 1] == 'W':
                        self.str_maze[ny - 1][c2x] = "┓"
                    elif solution[i + 1] == 'E':
                        self.str_maze[ny - 1][c2x] = "┏"
                y -= 1
            elif solution[i] == 'S':
                self.str_maze[sy][c2x] = "┃"
                if i < len(solution) - 1:
                    if solution[i + 1] == 'S':
                        self.str_maze[sy + 1][c2x] = "┃"
                    elif solution[i + 1] == 'W':
                        self.str_maze[sy + 1][c2x] = "┛"
                    elif solution[i + 1] == 'E':
                        self.str_maze[sy + 1][c2x] = "┗"
                y += 1
            elif solution[i] == 'W':
                self.str_maze[cy][c1x] = "━"
                self.str_maze[cy][wx] = "━"
                if i < len(solution) - 1:
                    if solution[i + 1] == 'N':
                        self.str_maze[cy][wx - 1] = "━"
                        self.str_maze[cy][wx - 2] = "┗"
                    elif solution[i + 1] == 'S':
                        self.str_maze[cy][wx - 1] = "━"
                        self.str_maze[cy][wx - 2] = "┏"
                    elif solution[i + 1] == 'W':
                        self.str_maze[cy][wx - 1] = "━"
                        self.str_maze[cy][wx - 2] = "━"
                x -= 1
            elif solution[i] == 'E':
                self.str_maze[cy][c3x] = "━"
                self.str_maze[cy][ex] = "━"
                if i < len(solution) - 1:
                    if solution[i + 1] == 'N':
                        self.str_maze[cy][ex + 1] = "━"
                        self.str_maze[cy][ex + 2] = "┛"
                    elif solution[i + 1] == 'S':
                        self.str_maze[cy][ex + 1] = "━"
                        self.str_maze[cy][ex + 2] = "┓"
                    elif solution[i + 1] == 'E':
                        self.str_maze[cy][ex + 1] = "━"
                        self.str_maze[cy][ex + 2] = "━"
                x += 1

    def pack_maze(self) -> None:
        """
        Coordinates the full assembly process of the maze canvas:
        initializes the canvas, generates walls, optionally adds the solution
        path, entry, exit, and the 42 brand elements.
        """
        self.canva_init()
        self.str_generate()
        if self.show_path:
            self.include_path()
            # print(self.path)
        self.include_entry()
        self.include_exit()
        self.fill_42()

    def rotate_colours(self) -> None:
        """
        Advances the internal colour index to cycle through the available
        ANSI color palette.
        """
        self.colour_index += 1

    def paint_maze(self) -> list[list[str]]:
        """
        Packs the maze structure and applies dynamic ANSI color formatting
        to each character based on the current colour index rotation.

        Returns:
            list[list[str]]: 2D grid containing the characters wrapped in
            ANSI color codes.
        """
        self.pack_maze()

        index_wall = self.colour_index % len(self.colours)
        index_42 = (self.colour_index + 1) % len(self.colours)
        index_ex = (self.colour_index + 2) % len(self.colours)
        index_path = (self.colour_index + 3) % len(self.colours)

        which_colour = list(self.colours.keys())
        colour_wall = self.colours[which_colour[index_wall]]
        colour_42 = self.colours[which_colour[index_42]]
        colour_ex = self.colours[which_colour[index_ex]]
        colour_path = self.colours[which_colour[index_path]]
        reset_colour: str = "\033[0m"

        painted_maze: list[list[str]] = []

        for y in range(len(self.str_maze)):
            painted_row: list[str] = []
            for x in range(len(self.str_maze[y])):
                char = self.str_maze[y][x]
                if char == "█":
                    painted_char: str = f"{colour_wall}{char}{reset_colour}"
                    painted_row.append(painted_char)
                elif char == "▓" or char == "▒":
                    painted_char = f"{colour_42}{char}{reset_colour}"
                    painted_row.append(painted_char)
                elif char == "E" or char == "X":
                    painted_char = f"{colour_ex}{char}{reset_colour}"
                    painted_row.append(painted_char)
                else:
                    painted_char = f"{colour_path}{char}{reset_colour}"
                    painted_row.append(painted_char)
            painted_maze.append(painted_row)
        return painted_maze

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the fully painted
        maze ready for terminal printing.
        """
        painted_maze = self.paint_maze()
        return ("\n".join("".join(painted_row) for painted_row
                          in painted_maze))

    def choice_menu(self) -> None:
        """
        Runs an interactive terminal menu allowing the user to regenerate
        the maze, toggle the solution path, rotate colors, or quit.
        """
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")
            str_choice = input("Choice? (1-4): ")
            try:
                choice = int(str_choice)
                if choice <= 0 or choice >= 5:
                    raise ValueError("You must choose between 1 and 4")
                elif choice == 1:
                    subprocess.run("cls" if os.name == "nt" else "clear",
                                   shell=True)
                    print("\nYou've chosen 1: generating a new maze\n")
                    self.generator.generate_maze(random.randint(1, 9999))
                    print(self)
                elif choice == 2:
                    if self.show_path:
                        self.show_path = False
                        subprocess.run("cls" if os.name == "nt" else "clear",
                                       shell=True)
                        print("\nYou've chosen 2: hiding the path\n")
                    else:
                        self.show_path = True
                        subprocess.run("cls" if os.name == "nt" else "clear",
                                       shell=True)
                        print("\nYou've chosen 2: showing the path\n")
                    print(self)
                elif choice == 3:
                    subprocess.run("cls" if os.name == "nt" else "clear",
                                   shell=True)
                    print("\nYou've chosen 3: rotating colours\n")
                    self.rotate_colours()
                    print(self)
                elif choice == 4:
                    print("\nYou've chosen 4: quitting the maze. Goodbye!\n")
                    break
            except ValueError as e:
                print(f"\nInvalid choice: {e}\n")

    def show_maze(self) -> None:
        """
        Prints the initial maze representation and launches the interactive
        menu loop.
        """
        print(self)
        self.choice_menu()


# def main() -> None:
#     try:
#         maze_structure = MazeGenerator(20, 20, (0, 0), (19, 1), False, 0)
#         maze_structure.generate_maze()
#         # solution = maze_structure.solve_maze()
#         maze_to_print = MazeDisplay(maze_structure)
#         maze_to_print.show_maze()

#     except ValueError as e:
#         print(e)


# if __name__ == "__main__":
#     main()
