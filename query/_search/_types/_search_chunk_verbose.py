from __future__ import annotations

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from .._types._search import SearchResult
from .._types._search_chunk import SearchResultChunk


class SearchResultChunkVerbose(SearchResultChunk):
    context_data: Optional[Union[str, List[Any], Dict[str, Any]]] = None
    """TODO: Documentation"""

    context_text: Optional[Union[str, List[str], Dict[str, str]]] = None
    """TODO: Documentation"""

    completion_time: Optional[float] = None
    """TODO: Documentation"""

    llm_calls: Optional[int] = None
    """TODO: Documentation"""

    map_result: Optional[List[SearchResult]] = None
    """TODO: Documentation"""

    reduce_context_data: Optional[Union[str, List[Any], Dict[str, Any]]] = None
    """TODO: Documentation"""

    reduce_context_text: Optional[Union[str, List[str], Dict[str, str]]] = None
    """TODO: Documentation"""
