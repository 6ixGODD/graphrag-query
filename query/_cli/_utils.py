# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from .. import errors as _errors


def parse_cli_err(err: _errors.CLIError) -> str:
    if isinstance(err, _errors.InvalidParameterError):
        return err.message
    return "An error occurred. Please try again later."
