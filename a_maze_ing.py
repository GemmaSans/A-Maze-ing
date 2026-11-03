from mazegen import MazeGenerator
from display import MazeDisplay
from config_parser import config_parser, ConfigError
from output import write_output, OutputError
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        config = config_parser(sys.argv[1])
        width = config["width"]
        height = config["height"]
        entry_pos = config["entry_pos"]
        exit_pos = config["exit_pos"]
        perfect = config["perfect"]
        seed = config.get("seed")

        maze_structure = MazeGenerator(width, height,
                                       entry_pos, exit_pos, perfect, seed)
        maze_structure.generate_maze()
        write_output(maze_structure, config["output_file"])
        maze_to_print = MazeDisplay(maze_structure)
        maze_to_print.show_maze()

    except (ConfigError, ValueError, OutputError) as e:
        print(e)


if __name__ == "__main__":
    main()
