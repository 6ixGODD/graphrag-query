# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


@dataclass
class VectorStoreDocument:
    """A document that is stored in vector storage."""

    id: Union[str, int]
    """unique id for the document"""

    text: Optional[str]
    """text content of the document"""

    vector: Optional[List[float]]
    """vector representation of the document"""

    attributes: Dict[str, Any] = field(default_factory=dict)
    """store any additional metadata, e.g. title, date ranges, etc"""


@dataclass
class VectorStoreSearchResult:
    """A vector storage search result."""

    document: VectorStoreDocument
    """Document that was found."""

    score: float
    """Similarity score between -1 and 1. Higher is more similar."""


class BaseVectorStore(ABC):
    """The base class for vector storage data-access classes."""
    collection_name: str
    kwargs: Dict[str, Any]

    def __init__(
        self,
        collection_name: str,
        **kwargs: Any,
    ):
        self.collection_name = collection_name
        self.kwargs = kwargs

    @abstractmethod
    def load_documents(
        self,
        documents: List[VectorStoreDocument],
        overwrite: bool = True
    ) -> None:
        """Load documents into the vector-store."""
        ...

    @abstractmethod
    def similarity_search_by_vector(
        self,
        query_embedding: List[float],
        k: int = 10,
        **kwargs: Any
    ) -> List[VectorStoreSearchResult]:
        """Perform ANN search by vector."""
        ...

    @abstractmethod
    def similarity_search_by_text(
        self,
        text: str,
        text_embedder: Callable[[str], List[float]],
        k: int = 10,
        **kwargs: Any
    ) -> List[VectorStoreSearchResult]:
        """Perform ANN search by text."""
        ...

    @abstractmethod
    def filter_by_id(self, include_ids: Union[List[str], List[int]]) -> Any:
        """Build a query filter to filter documents by id."""
        ...
