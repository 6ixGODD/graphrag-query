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

import abc
import dataclasses
import typing


# TODO: Instead of using dataclasses, use pydantic models?
@dataclasses.dataclass
class VectorStoreDocument:
    """A document that is stored in vector storage."""

    id: typing.Union[str, int]
    """unique id for the document"""

    text: typing.Optional[str]
    """text content of the document"""

    vector: typing.Optional[typing.List[float]]
    """vector representation of the document"""

    attributes: typing.Dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    """store any additional metadata, e.g. title, date ranges, etc"""


@dataclasses.dataclass
class VectorStoreSearchResult:
    """A vector storage search result."""

    document: VectorStoreDocument
    """Document that was found."""

    score: float
    """Similarity score between -1 and 1. Higher is more similar."""


class BaseVectorStore(abc.ABC):
    """The base class for vector storage data-access classes."""
    collection_name: str
    kwargs: typing.Dict[str, typing.Any]

    def __init__(
        self,
        collection_name: str,
        **kwargs: typing.Any,
    ):
        self.collection_name = collection_name
        self.kwargs = kwargs

    @abc.abstractmethod
    def load_documents(
        self,
        documents: typing.List[VectorStoreDocument],
        overwrite: bool = True
    ) -> None:
        """Load documents into the vector-store."""
        ...

    @abc.abstractmethod
    def similarity_search_by_vector(
        self,
        query_embedding: typing.List[float],
        k: int = 10,
        **kwargs: typing.Any
    ) -> typing.List[VectorStoreSearchResult]:
        """Perform ANN search by vector."""
        ...

    @abc.abstractmethod
    def similarity_search_by_text(
        self,
        text: str,
        text_embedder: typing.Callable[[str], typing.List[float]],
        k: int = 10,
        **kwargs: typing.Any
    ) -> typing.List[VectorStoreSearchResult]:
        """Perform ANN search by text."""
        ...

    @abc.abstractmethod
    def filter_by_id(self, include_ids: typing.Union[typing.List[str], typing.List[int]]) -> typing.Any:
        """Build a query filter to filter documents by id."""
        ...
