from mazegen import MazeGenerator
from display import MazeDisplay


def main() -> None:
    try:
        maze_structure = MazeGenerator(20, 20, (0, 0), (19, 1), False, 0)
        maze_structure.generate_maze()
        # solution = maze_structure.solve_maze()
        maze_to_print = MazeDisplay(maze_structure)
        maze_to_print.show_maze()

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
