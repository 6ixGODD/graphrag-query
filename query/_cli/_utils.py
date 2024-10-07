# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import datetime
import string
import sys
import typing

import typing_extensions

from .. import (
    errors as _errors,
    types as _types,
)


class ANSIFormatter:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'

    @classmethod
    def format(cls, text: str, *styles: str) -> str:
        return f"{''.join(styles)}{text}{cls.RESET}"


class SaveFormatter(string.Formatter):
    @typing_extensions.override
    def get_value(self, key: typing.Union[int, str], args: typing.Any, kwargs: typing.Any) -> typing.Any:
        if isinstance(key, int):
            if key < len(args):
                return args[key]
            else:
                return "<missing>"
        # Handle keyword arguments
        else:
            return kwargs.get(key, "<missing>")

    @typing_extensions.override
    def format_field(self, value: typing.Any, format_spec: str) -> str:
        try:
            return super().format_field(value, format_spec)
        except (KeyError, ValueError):
            return str(value)


class CLILogger(_types.Logger):

    @staticmethod
    def _safe_format(msg: str, *args: typing.Any, **kwargs: typing.Any) -> str:
        formatter = SaveFormatter()
        return formatter.format(msg, *args, **kwargs)

    def _log(self, level: str, color: str, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        timestamp = ANSIFormatter.format(str(datetime.datetime.now()), ANSIFormatter.GREEN)
        level_str = ANSIFormatter.format(f" [{level.ljust(8)}] ", color)
        formatted_msg = ANSIFormatter.format(self._safe_format(msg, *args, **kwargs), color, ANSIFormatter.BOLD)
        sys.stdout.write(f"{timestamp} {level_str} {formatted_msg}\n")
        sys.stdout.flush()

    def error(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._log("ERROR", ANSIFormatter.RED, msg, *args, **kwargs)

    def warning(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._log("WARNING", ANSIFormatter.YELLOW, msg, *args, **kwargs)

    def info(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._log("INFO", ANSIFormatter.BLUE, msg, *args, **kwargs)

    def debug(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._log("DEBUG", ANSIFormatter.CYAN, msg, *args, **kwargs)


def parse_cli_err(err: _errors.CLIError) -> str:
    if isinstance(err, _errors.InvalidParameterError):
        return err.message
    return "An error occurred. Please try again later."
