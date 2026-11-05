from mazegen import MazeGenerator
from display import MazeDisplay, DisplayError
from parse_config import config_parser, ConfigError
from output import write_output, OutputError
import sys


def main() -> None:
    """
    Entry point of the program.

    Reads the configuration file given on the command line, generates a
    maze from it, writes the maze to the output file defined in the
    configuration, and shows it in the interactive display.

    The only command-line argument is the path to the config file:
    python3 a_maze_ing.py <config_file>

    Errors raised while reading the configuration (ConfigError), building
    the maze (ValueError), writing the output file (OutputError) or showing
    the maze (DisplayError) are caught and printed as a message instead of
    a traceback.

    Raises:
        SystemExit: with status 1 if the wrong number of arguments is
            given.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        config = config_parser(sys.argv[1])
        seed = config.get("seed")

        maze_structure = MazeGenerator(config["width"],
                                       config["height"],
                                       config["entry_pos"],
                                       config["exit_pos"],
                                       config["perfect"], seed)
        maze_structure.generate_maze()
        write_output(maze_structure, config["output_file"])
        maze_to_print = MazeDisplay(maze_structure, maze_structure.solution)
        maze_to_print.show_maze()

    except (ConfigError, ValueError, OutputError, DisplayError) as e:
        print(e)


if __name__ == "__main__":
    main()
