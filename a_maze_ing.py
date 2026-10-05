MIN_WIDTH = 9
MIN_HEIGHT = 7


class MazeGenerator():
    """Class for the generation of mazes"""
    def __init__(self,
                 width: int,
                 height: int,
                 entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int],
                 is_perfect: bool,
                 seed: int) -> None:
        """
        Initialization of the MazeGenerator class.

        Parameters:
            width (int): width of the maze
            height (int): height of the maze
            entry_pos (tuple(int, int)): position of the entry of the maze
            exit_pos (tuple(int, int)): position of the exit of the maze
            is_perfect (bool): True if the maze is perfect, False otherwise
            seed (int): seed for reproducibility
        """
        if width < 1:
            raise ValueError("Width needs to be larger")
        if height < 1:
            raise ValueError("Height needs to be larger")
        if exit_pos == entry_pos:
            raise ValueError("Entry and exit on same cell")
        if any((entry_pos[0] < 0, entry_pos[0] >= width,
               entry_pos[1] < 0, entry_pos[1] >= height)):
            raise ValueError("Entry position off limits")
        if any((exit_pos[0] < 0, exit_pos[0] >= width,
               exit_pos[1] < 0, exit_pos[1] >= height)):
            raise ValueError("Exit position off limits")

        self.width = width
        self.height = height
        self.entry = entry_pos
        self.exit = exit_pos
        self.is_perfect = is_perfect
        self.seed = seed
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            self.has_42 = False
        else:
            self.has_42 = True

    def generate(self) -> None:
        pass
