# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

import warnings
import typing

from . import (
    types as _types,
    _version,
)

__all__ = [
    'get_default_logger',
]

_default_logger: _types.Logger
_loguru: typing.Any  # for type checking

try:
    import loguru as _loguru

    _default_logger = _loguru.logger.bind(namespace=f'{_version.__title__}:{_version.__version__}')

except ImportError:
    _loguru = None
    warnings.warn('Required package "loguru" not found. Using default logger instead.')

    import logging as _logging

    # noinspection PyTypeChecker
    _default_logger = _logging.getLogger(f'{_version.__title__}:{_version.__version__}')


def get_default_logger() -> _types.Logger:
    return _default_logger
