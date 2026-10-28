class ConfigError(Exception):
    """Raised when the config file is missing or invalid."""


class OutputError(Exception):
    """Raised when the output file cannot be created or written"""
