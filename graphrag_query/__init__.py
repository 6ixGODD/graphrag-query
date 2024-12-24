# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

import importlib
import typing

from . import (
    errors,
    types,
)
from ._client import (
    AsyncGraphRAGClient,
    GraphRAGClient,
)
from ._config import (
    ChatLLMConfig,
    ContextConfig,
    EmbeddingConfig,
    GlobalSearchConfig,
    GraphRAGConfig,
    LocalSearchConfig,
    LoggingConfig,
)
from ._search import (
    AsyncChatLLM,
    AsyncEmbedding,
    AsyncGlobalSearchEngine,
    AsyncLocalSearchEngine,
    AsyncQueryEngine,
    BaseAsyncChatLLM,
    BaseAsyncEmbedding,
    BaseChatLLM,
    BaseContextBuilder,
    BaseEmbedding,
    ChatLLM,
    Embedding,
    GlobalContextBuilder,
    GlobalContextLoader,
    GlobalSearchEngine,
    LocalContextBuilder,
    LocalContextLoader,
    LocalSearchEngine,
    QueryEngine,
    SearchResult,
    SearchResultChunk,
    SearchResultChunkVerbose,
    SearchResultVerbose,
)
from ._version import (
    __title__,
    __version__,
)

__all__ = [
    "errors",
    "types",

    "AsyncGraphRAGClient",
    "GraphRAGClient",

    "ChatLLMConfig",
    "ContextConfig",
    "EmbeddingConfig",
    "GlobalSearchConfig",
    "GraphRAGConfig",
    "LocalSearchConfig",
    "LoggingConfig",

    "AsyncChatLLM",
    "AsyncEmbedding",
    "AsyncGlobalSearchEngine",
    "AsyncLocalSearchEngine",
    "AsyncQueryEngine",
    "BaseAsyncChatLLM",
    "BaseAsyncEmbedding",
    "BaseChatLLM",
    "BaseContextBuilder",
    "BaseEmbedding",
    "ChatLLM",
    "Embedding",
    "GlobalContextBuilder",
    "GlobalContextLoader",
    "GlobalSearchEngine",
    "LocalContextBuilder",
    "LocalContextLoader",
    "LocalSearchEngine",
    "QueryEngine",
    "SearchResult",
    "SearchResultChunk",
    "SearchResultChunkVerbose",
    "SearchResultVerbose",

    "__title__",
    "__version__",
]


# Copied from https://peps.python.org/pep-0562/
def __getattr__(name: str) -> typing.Any:
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
