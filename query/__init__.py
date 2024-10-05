# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import importlib
import typing

from . import _client
from . import _config
from . import _search
from . import _version

__title__ = _version.__title__
__version__ = _version.__version__

GraphRAGClient = _client.GraphRAGClient
AsyncGraphRAGClient = _client.AsyncGraphRAGClient

QueryEngine = _search.QueryEngine
AsyncQueryEngine = _search.AsyncQueryEngine
LocalSearchEngine = _search.LocalSearchEngine
GlobalSearchEngine = _search.GlobalSearchEngine
AsyncLocalSearchEngine = _search.AsyncLocalSearchEngine
AsyncGlobalSearchEngine = _search.AsyncGlobalSearchEngine
BaseContextBuilder = _search.BaseContextBuilder
LocalContextBuilder = _search.LocalContextBuilder
GlobalContextBuilder = _search.GlobalContextBuilder
LocalContextLoader = _search.LocalContextLoader
GlobalContextLoader = _search.GlobalContextLoader

ChatLLMConfig = _config.ChatLLMConfig
EmbeddingConfig = _config.EmbeddingConfig
LoggingConfig = _config.LoggingConfig
ContextConfig = _config.ContextConfig
LocalSearchConfig = _config.LocalSearchConfig
GlobalSearchConfig = _config.GlobalSearchConfig
GraphRAGConfig = _config.GraphRAGConfig

__all__ = [
    "__title__",
    "__version__",

    "GraphRAGClient",
    "AsyncGraphRAGClient",

    "QueryEngine",
    "AsyncQueryEngine",
    "LocalSearchEngine",
    "GlobalSearchEngine",
    "AsyncLocalSearchEngine",
    "AsyncGlobalSearchEngine",
    "BaseContextBuilder",
    "LocalContextBuilder",
    "GlobalContextBuilder",
    "LocalContextLoader",
    "GlobalContextLoader",

    'ChatLLMConfig',
    'EmbeddingConfig',
    'LoggingConfig',
    'ContextConfig',
    'LocalSearchConfig',
    'GlobalSearchConfig',
    'GraphRAGConfig',
]


# Copied from https://peps.python.org/pep-0562/
def __getattr__(name: str) -> typing.Any:
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
