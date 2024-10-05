# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.
#
# Copyright (c) 2024 6ixGODD.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import importlib
import typing

from .._search import _context
from .._search import _engine
from .._search import _llm
from .._search import _model
from .._search import _types

BaseContextBuilder = _context.BaseContextBuilder
GlobalContextBuilder = _context.GlobalContextBuilder
LocalContextBuilder = _context.LocalContextBuilder
ConversationHistory = _context.ConversationHistory
ConversationRole = _context.ConversationRole
ConversationTurn = _context.ConversationTurn
BaseContextLoader = _context.BaseContextLoader
GlobalContextLoader = _context.GlobalContextLoader
LocalContextLoader = _context.LocalContextLoader

AsyncQueryEngine = _engine.AsyncQueryEngine
QueryEngine = _engine.QueryEngine
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
