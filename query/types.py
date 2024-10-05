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

from ._search._llm import _types as _llm_types
from ._search import _types

MessageParam_T: typing.TypeAlias = _llm_types.MessageParam_T

__all__ = [
    'Logger',
    'Response',
    'ResponseVerbose',
    'ResponseChunk',
    'ResponseChunkVerbose',
    'MessageParam_T',
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
