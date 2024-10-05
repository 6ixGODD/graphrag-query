# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import importlib
import typing

from .._search import _base_engine
from .._search import _context
from .._search import _engine
from .._search import _llm
from .._search import _model
from .._search import _types

AsyncQueryEngine = _base_engine.AsyncQueryEngine
QueryEngine = _base_engine.QueryEngine
BaseContextBuilder = _context.BaseContextBuilder
GlobalContextBuilder = _context.GlobalContextBuilder
LocalContextBuilder = _context.LocalContextBuilder
ConversationHistory = _context.ConversationHistory
ConversationRole = _context.ConversationRole
ConversationTurn = _context.ConversationTurn
BaseContextLoader = _context.BaseContextLoader
GlobalContextLoader = _context.GlobalContextLoader
LocalContextLoader = _context.LocalContextLoader
AsyncGlobalSearchEngine = _engine.AsyncGlobalSearchEngine
AsyncLocalSearchEngine = _engine.AsyncLocalSearchEngine
GlobalSearchEngine = _engine.GlobalSearchEngine
LocalSearchEngine = _engine.LocalSearchEngine
AsyncChatLLM = _llm.AsyncChatLLM
AsyncEmbedding = _llm.AsyncEmbedding
BaseAsyncChatLLM = _llm.BaseAsyncChatLLM
BaseAsyncEmbedding = _llm.BaseAsyncEmbedding
BaseChatLLM = _llm.BaseChatLLM
BaseEmbedding = _llm.BaseEmbedding
ChatLLM = _llm.ChatLLM
Embedding = _llm.Embedding
Community = _model.Community
CommunityReport = _model.CommunityReport
Covariate = _model.Covariate
Document = _model.Document
Entity = _model.Entity
Identified = _model.Identified
Named = _model.Named
Relationship = _model.Relationship
TextUnit = _model.TextUnit
SearchResult = _types.SearchResult
SearchResultChunk = _types.SearchResultChunk
SearchResultChunkVerbose = _types.SearchResultChunkVerbose
SearchResultVerbose = _types.SearchResultVerbose

__all__ = [
    "AsyncQueryEngine",
    "QueryEngine",
    "BaseContextBuilder",
    "GlobalContextBuilder",
    "LocalContextBuilder",
    "ConversationHistory",
    "ConversationRole",
    "ConversationTurn",
    "BaseContextLoader",
    "GlobalContextLoader",
    "LocalContextLoader",
    "AsyncGlobalSearchEngine",
    "AsyncLocalSearchEngine",
    "GlobalSearchEngine",
    "LocalSearchEngine",
    "AsyncChatLLM",
    "AsyncEmbedding",
    "BaseAsyncChatLLM",
    "BaseAsyncEmbedding",
    "BaseChatLLM",
    "BaseEmbedding",
    "ChatLLM",
    "Embedding",
    "Community",
    "CommunityReport",
    "Covariate",
    "Document",
    "Entity",
    "Identified",
    "Named",
    "Relationship",
    "TextUnit",
    "SearchResult",
    "SearchResultChunk",
    "SearchResultChunkVerbose",
    "SearchResultVerbose",
]


# Copied from https://peps.python.org/pep-0562/
def __getattr__(name: str) -> typing.Any:
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
