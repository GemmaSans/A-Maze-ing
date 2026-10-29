from typing import NotRequired, TypedDict


MANDATORY_KEYS: set[str] = {"WIDTH", "HEIGHT", "ENTRY",
                            "EXIT", "OUTPUT_FILE", "PERFECT"}
OPTIONAL_KEYS: set[str] = {"SEED"}


class ConfigError(Exception):
    """Raised when the config file is missing or invalid."""


class MazeConfig(TypedDict):
    """
    Typed container for the validated maze configuration.

    Fields:
        width (int): width of the maze, in cells.
        height (int): height of the maze, in cells.
        entry_pos (tuple(int, int)): entry coordinates (x, y).
        exit_pos (tuple(int, int)): exit coordinates (x, y).
        output_file (str): name of the file the maze is written to.
        perfect (bool): True if the maze must be perfect.
        seed (int): optional seed for reproducibility.
    """
    width: int
    height: int
    entry_pos: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    perfect: bool
    seed: NotRequired[int]


def _parse_int(key: str, value: str) -> int:
    """
    Converts a config value to an integer.

    Parameters:
        key (str): name of the config key, used in error messages.
        value (str): the raw text value.

    Returns:
        int: the converted value.

    Raises:
        ConfigError: if the value is not a valid integer.
    """
    try:
        checked = int(value)
        return checked
    except ValueError:
        raise ConfigError(f"{key}: {value} is not an int.")


def _parse_tuple(key: str, value: str) -> tuple[int, int]:
    """
    Converts a config value such as '3,4' to a pair of integers.

    Parameters:
        key (str): name of the config key, used in error messages.
        value (str): the raw text value.

    Returns:
        tuple(int, int): the (x, y) coordinates.

    Raises:
        ConfigError: if the value is not exactly two comma-separated
            integers.
    """
    coord = value.split(",")
    if len(coord) != 2:
        raise ConfigError(f"{key}: {value} is not a tuple(int, int)")
    try:
        x = int(coord[0])
        y = int(coord[1])
        return (x, y)
    except ValueError:
        raise ConfigError(f"{key}: {value} is not a tuple(int, int)")


def _parse_bool(key: str, value: str) -> bool:
    """
    Converts a config value to a boolean. Only 'True' and 'False' are
    accepted.

    Parameters:
        key (str): name of the config key, used in error messages.
        value (str): the raw text value.

    Returns:
        bool: the converted value.

    Raises:
        ConfigError: if the value is neither 'True' nor 'False'.
    """
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ConfigError(f"{key}: {value} is not a bool")


def _read_file(file: str) -> dict[str, str]:
    """
    Reads the config file and returns its raw KEY=VALUE pairs.

    Blank lines and lines starting with '#' are ignored. Only keys in
    MANDATORY_KEYS and OPTIONAL_KEYS are accepted.

    Parameters:
        file (str): the name of the config file.

    Returns:
        dict(str, str): the keys and their raw string values.

    Raises:
        ConfigError: if the file cannot be read, a line is malformed, a
            key is unknown or duplicated, or a mandatory key is missing.
    """
    config_dict: dict[str, str] = {}
    try:
        with open(file, encoding="utf-8") as f:
            for num, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    if not key:
                        raise ConfigError(f"Line {num}: empty key")
                    if key not in MANDATORY_KEYS | OPTIONAL_KEYS:
                        raise ConfigError(f"Line {num}: unknown key '{key}'")
                    if key in config_dict:
                        raise ConfigError(f"Line {num}: duplicate key '{key}'")
                    config_dict[key] = value
                else:
                    raise ConfigError(f"Line {num}: expected KEY=VALUE, "
                                      f"got '{line}'")
    except (OSError, UnicodeDecodeError) as e:
        raise ConfigError(f"Cannot open or read '{file}': {e}")
    missing = MANDATORY_KEYS - config_dict.keys()
    if missing:
        raise ConfigError(f"Mandatory keys are missing: {', '.join(missing)}")
    return config_dict


def config_parser(file: str) -> MazeConfig:
    """
    Reads a config file and converts its values to their proper types.

    Parameters:
        file (str): the name of the config file.

    Returns:
        MazeConfig: the validated configuration. 'seed' is only present if
        SEED was given in the file.

    Raises:
        ConfigError: if the file or any of its values is invalid.
    """
    raw_config = _read_file(file)
    width = _parse_int("WIDTH", raw_config["WIDTH"])
    height = _parse_int("HEIGHT", raw_config["HEIGHT"])
    entry_pos = _parse_tuple("ENTRY", raw_config["ENTRY"])
    exit_pos = _parse_tuple("EXIT", raw_config["EXIT"])
    output_file = raw_config["OUTPUT_FILE"]
    if not output_file:
        raise ConfigError("OUTPUT_FILE is empty")
    perfect = _parse_bool("PERFECT", raw_config["PERFECT"])
    config = MazeConfig(
        width=width,
        height=height,
        entry_pos=entry_pos,
        exit_pos=exit_pos,
        output_file=output_file,
        perfect=perfect,
    )
    if "SEED" in raw_config:
        config["seed"] = _parse_int("SEED", raw_config["SEED"])
    return config
