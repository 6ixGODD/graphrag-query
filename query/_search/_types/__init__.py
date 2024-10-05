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
