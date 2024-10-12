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


class SafeFormatter(string.Formatter):
    @typing_extensions.override
    def format(self, __format_string: str, /, *args: typing.Any, **kwargs: typing.Any) -> str:
        result = ''

        try:
            for literal_text, field_name, format_spec, conversion in self.parse(__format_string):
                # Append the literal text
                result += literal_text

                # If there's a field, process it
                if field_name is not None:
                    try:
                        # Get the value
                        obj = self.get_value(field_name, args, kwargs)
                        # Convert and format the field
                        obj = self.convert_field(obj, conversion)
                        formatted = self.format_field(obj, format_spec or '')
                        result += formatted
                    except (KeyError, IndexError):
                        # Reconstruct the placeholder and leave it as is
                        placeholder = '{' + field_name
                        if conversion:
                            placeholder += '!' + conversion
                        if format_spec:
                            placeholder += ':' + format_spec
                        placeholder += '}'
                        result += placeholder
        except ValueError:
            result = __format_string
        return result

    @typing_extensions.override
    def get_value(
        self,
        key: typing.Union[int, str],
        args: typing.Sequence[typing.Any],
        kwargs: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        if isinstance(key, int):
            if key < len(args):
                return args[key]
            else:
                raise IndexError(key)
        else:
            return kwargs[key]

    @typing_extensions.override
    def format_field(self, value: typing.Any, format_spec: str) -> str:
        try:
            return super().format_field(value, format_spec)
        except (KeyError, ValueError):
            return str(value)


class CLILogger(_types.Logger):

    @staticmethod
    def _safe_format(msg: str, *args: typing.Any, **kwargs: typing.Any) -> str:
        formatter = SafeFormatter()
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
    if isinstance(err, _errors.InvalidParameterError) or isinstance(err, _errors.MissingPackageError):
        return err.message
    return "An error occurred. Please try again later."


if __name__ == '__main__':
    fmt = SafeFormatter()
    print(fmt.format("Hello, {0}!", "world"))
    print(fmt.format("Hello, {name}!", name="world"))
    print(fmt.format("Hello, {0}! You have {1} new messages.", "world", 5))
    print(fmt.format("Hello, {name}! You have {count} new messages.", name="world", count=5))
    print(fmt.format("{{{{{}", "world"))
    print(fmt.format("{{{{name}}", name="world"))
    print(fmt.format("{'name': 'world'}", name="world"))
    print(fmt.format("{'name': 'world'}}", name="world"))
