# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import os
import pathlib
import typing

import graphrag_query
from graphrag_query import types

_client: graphrag_query.AsyncGraphRAGClient


def init_client(config_file: typing.Union[str, os.PathLike[str], pathlib.Path]) -> None:
    global _client
    _client = graphrag_query.AsyncGraphRAGClient.from_config_file(config_file)


def get_client(logger: typing.Optional[types.Logger]) -> graphrag_query.AsyncGraphRAGClient:
    global _client
    _client.logger = logger
    return _client
