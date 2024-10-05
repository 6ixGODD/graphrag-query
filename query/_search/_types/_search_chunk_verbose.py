from __future__ import annotations

import typing

from .._types import _search, _search_chunk


class SearchResultChunkVerbose(_search_chunk.SearchResultChunk):
    context_data: typing.Optional[typing.Union[str, typing.List[typing.Any], typing.Dict[str, typing.Any]]] = None
    """TODO: Documentation"""

    context_text: typing.Optional[typing.Union[str, typing.List[str], typing.Dict[str, str]]] = None
    """TODO: Documentation"""

    completion_time: typing.Optional[float] = None
    """TODO: Documentation"""

    llm_calls: typing.Optional[int] = None
    """TODO: Documentation"""

    map_result: typing.Optional[typing.List[_search.SearchResult]] = None
    """TODO: Documentation"""

    reduce_context_data: typing.Optional[
        typing.Union[str, typing.List[typing.Any], typing.Dict[str, typing.Any]]] = None
    """TODO: Documentation"""

    reduce_context_text: typing.Optional[typing.Union[str, typing.List[str], typing.Dict[str, str]]] = None
    """TODO: Documentation"""
