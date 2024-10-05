# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

import typing

from ..._search import _context
from ..._search._types import _search
from ..._search._types import _search_chunk
from ..._search._types import _search_chunk_verbose
from ..._search._types import _search_verbose

Choice = _search.Choice
Message = _search.Message
SearchResult = _search.SearchResult
Usage = _search.Usage
ChunkChoice = _search_chunk.ChunkChoice
Delta = _search_chunk.Delta
SearchResultChunk = _search_chunk.SearchResultChunk
SearchResultChunkVerbose = _search_chunk_verbose.SearchResultChunkVerbose
SearchResultVerbose = _search_verbose.SearchResultVerbose

__all__ = [
    "SearchResult",
    "Choice",
    "Message",
    "Usage",
    "SearchResultChunk",
    "ChunkChoice",
    "Delta",
    "SearchResultChunkVerbose",
    "SearchResultVerbose",
]

SearchResult_T: typing.TypeAlias = typing.Union[SearchResult, SearchResultVerbose]

StreamSearchResult_T: typing.TypeAlias = typing.Generator[
    typing.Union[SearchResultChunk, SearchResultChunkVerbose], None, None
]

AsyncStreamSearchResult_T: typing.TypeAlias = typing.AsyncGenerator[
    typing.Union[SearchResultChunk, SearchResultChunkVerbose], None
]

ConversationHistory_T: typing.TypeAlias = typing.Union[
    _context.ConversationHistory,
    typing.List[typing.Dict[typing.Literal["role", "content"], str]],
    None,
]
