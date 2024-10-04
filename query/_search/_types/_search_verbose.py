from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from ..._search._types._search import SearchResult


class SearchResultVerbose(SearchResult):
    context_data: Optional[Union[str, List[Any], Dict[str, Any]]] = None
    """TODO: Documentation"""

    context_text: Optional[Union[str, List[str], Dict[str, str]]] = None
    """TODO: Documentation"""

    completion_time: float
    """TODO: Documentation"""

    llm_calls: int
    """TODO: Documentation"""

    map_result: Optional[List[SearchResult]] = None
    """TODO: Documentation"""

    reduce_context_data: Optional[Union[str, List[Any], Dict[str, Any]]] = None
    """TODO: Documentation"""

    reduce_context_text: Optional[Union[str, List[str], Dict[str, str]]] = None
    """TODO: Documentation"""
