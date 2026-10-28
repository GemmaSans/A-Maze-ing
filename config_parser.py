from typing import NotRequired, TypedDict
import sys


class ConfigError(Exception):
    """Raised when the config file is missing or invalid."""


class MazeConfig(TypedDict):
    width: int
    height: int
    entry_pos: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    perfect: bool
    seed: NotRequired[int]


MANDATORY_KEYS: set[str] = {"WIDTH", "HEIGHT", "ENTRY",
                            "EXIT", "OUTPUT_FILE", "PERFECT"}
OPTIONAL_KEYS: set[str] = {"SEED"}


def _parse_int(key: str, value: str) -> int:
    try:
        checked = int(value)
        return checked
    except ValueError:
        raise ConfigError(f"{key}: {value} is not an int.")


def _parse_tuple(key: str, value: str) -> tuple[int, int]:
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
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ConfigError(f"{key}: {value} is not a bool")


def _read_file(file: str) -> dict[str, str]:
    """
    Takes the name of a file and parses through it, accepting only
    KEY=VALUE format of keys in MANDATORY_KEYS and OPTIONAL_KEYS.
    Raises ConfigError if a value is not accepted.

    Parameters:
        file (str): the name of the config file.

    Returns:
        dict(str, str): a dictionary of key=values.
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


if __name__ == "__main__":
    try:
        config = config_parser(sys.argv[1])
        print(config)
    except Exception as e:
        print(e)
