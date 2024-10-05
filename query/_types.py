from __future__ import annotations

import typing

from ._search._llm import _types as _llm_types
from ._search import _types

MessageParam_T: typing.TypeAlias = _llm_types.MessageParam_T

__all__ = [
    'MessageParam_T',
    'Logger',
    'Response',
    'ResponseVerbose',
    'ResponseChunk',
    'ResponseChunkVerbose',
    'Response_T',
    'StreamResponse_T',
    'AsyncStreamResponse_T',
]


class Logger(typing.Protocol):
    def error(self, msg: str, *args, **kwargs: typing.Any) -> None: ...

    def warning(self, msg: str, *args, **kwargs: typing.Any) -> None: ...

    def info(self, msg: str, *args, **kwargs: typing.Any) -> None: ...

    def debug(self, msg: str, *args, **kwargs: typing.Any) -> None: ...


Response: typing.TypeAlias = _types.SearchResult
ResponseVerbose: typing.TypeAlias = _types.SearchResultVerbose
ResponseChunk: typing.TypeAlias = _types.SearchResultChunk
ResponseChunkVerbose: typing.TypeAlias = _types.SearchResultChunkVerbose

Response_T: typing.TypeAlias = typing.Union[Response, ResponseVerbose]
_Response_Chunk_T: typing.TypeAlias = typing.Union[ResponseChunk, ResponseChunkVerbose]
StreamResponse_T: typing.TypeAlias = typing.Generator[_Response_Chunk_T, None, None]
AsyncStreamResponse_T: typing.TypeAlias = typing.AsyncGenerator[_Response_Chunk_T, None]
