from __future__ import annotations

import typing

from ..._search._types import _search


class SearchResultVerbose(_search.SearchResult):
    context_data: typing.Optional[typing.Union[str, typing.List[typing.Any], typing.Dict[str, typing.Any]]] = None
    """TODO: Documentation"""

    context_text: typing.Optional[typing.Union[str, typing.List[str], typing.Dict[str, str]]] = None
    """TODO: Documentation"""

    completion_time: float
    """TODO: Documentation"""

    llm_calls: int
    """TODO: Documentation"""

    map_result: typing.Optional[typing.List[_search.SearchResult]] = None
    """TODO: Documentation"""

    reduce_context_data: typing.Optional[
        typing.Union[str, typing.List[typing.Any], typing.Dict[str, typing.Any]]] = None
    """TODO: Documentation"""

    reduce_context_text: typing.Optional[typing.Union[str, typing.List[str], typing.Dict[str, str]]] = None
    """TODO: Documentation"""
