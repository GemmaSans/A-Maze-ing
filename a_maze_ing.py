from mazegen import MazeGenerator
from display import MazeDisplay
from config_parser import config_parser, ConfigError
from output_txt import write_output, OutputError


def main() -> None:
    try:
        config = config_parser("config.txt")
        width = config["width"]
        height = config["height"]
        entry_pos = config["entry_pos"]
        exit_pos = config["exit_pos"]
        perfect = config["perfect"]
        seed = config["seed"]

        maze_structure = MazeGenerator(width, height,
                                       entry_pos, exit_pos, perfect, seed)
        maze_structure.generate_maze()
        solution = maze_structure.solve_maze()
        write_output(maze_structure, config["output_file"], solution)
        maze_to_print = MazeDisplay(maze_structure)
        maze_to_print.show_maze()

    except (ConfigError, ValueError, OutputError) as e:
        print(e)


if __name__ == "__main__":
    main()
