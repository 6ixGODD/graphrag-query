# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import fastapi
from ._logging import LoggingMiddleware
from ._context import ContextMiddleware
from ._auth import AuthMiddleware


# noinspection PyTypeChecker
def init_middleware(app: fastapi.FastAPI, *, api_keys: typing.List[str]) -> None:
    app.add_middleware(AuthMiddleware, api_keys=api_keys)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ContextMiddleware)

