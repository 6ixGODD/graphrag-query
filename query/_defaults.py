from __future__ import annotations

import warnings
from typing import Any

__all__ = [
    'get_default_logger',
]

_default_logger: Any
_loguru: Any
try:
    import loguru as _loguru

    _default_logger = _loguru.logger.bind(name=__name__)

except ImportError:
    _loguru = None
    warnings.warn('Required package "loguru" not found. Using default logger instead.')

    import logging as _logging

    _default_logger = _logging.getLogger(__name__)


def get_default_logger() -> _default_logger.__class__:
    return _default_logger
