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
