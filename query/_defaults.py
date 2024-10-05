from __future__ import annotations

import warnings
import typing

from . import _types

__all__ = [
    'get_default_logger',
]

_default_logger: _types.Logger
_loguru: typing.Any  # for type hinting

try:
    import loguru as _loguru

    _default_logger = _loguru.logger.bind(name=__name__)

except ImportError:
    _loguru = None
    warnings.warn('Required package "loguru" not found. Using default logger instead.')

    import logging as _logging

    # noinspection PyTypeChecker
    _default_logger = _logging.getLogger(__name__)


def get_default_logger() -> _types.Logger:
    return _default_logger
