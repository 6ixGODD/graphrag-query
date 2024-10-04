from __future__ import annotations

from typing import (
    AsyncGenerator,
    Dict,
    Generator,
    List,
    Literal,
    TypeAlias,
    Union,
)

from ..._search import _context
from ..._search._types._search import Choice, Message, SearchResult, Usage
from ..._search._types._search_chunk import ChunkChoice, Delta, SearchResultChunk
from ..._search._types._search_chunk_verbose import SearchResultChunkVerbose
from ..._search._types._search_verbose import SearchResultVerbose

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

SearchResult_T: TypeAlias = Union[SearchResult, SearchResultVerbose]

StreamSearchResult_T: TypeAlias = Generator[Union[SearchResultChunk, SearchResultChunkVerbose], None, None]

AsyncStreamSearchResult_T: TypeAlias = AsyncGenerator[Union[SearchResultChunk, SearchResultChunkVerbose], None]

ConversationHistory_T: TypeAlias = Union[
    _context.ConversationHistory,
    List[Dict[Literal["role", "content"], str]],
    None,
]
