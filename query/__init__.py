# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

from . import _errors
from . import _version

GraphRAGError: typing.Type[Exception] = _errors.GraphRAGError
__title__ = _version.__title__
__version__ = _version.__version__

__all__ = [
    "GraphRAGError",
    "__title__",
    "__version__",
]
