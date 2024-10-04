# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from typing import Any, Dict, List, Optional

from ..._search._model._named import Named


class Entity(Named):
    """A protocol for an entity in the system."""

    type: Optional[str] = None
    """Type of the entity (can be any string, optional)."""

    description: Optional[str] = None
    """Description of the entity (optional)."""

    description_embedding: Optional[List[float]] = None
    """The semantic (i.e. text) embedding of the entity (optional)."""

    name_embedding: Optional[List[float]] = None
    """The semantic (i.e. text) embedding of the entity (optional)."""

    graph_embedding: Optional[List[float]] = None
    """The graph embedding of the entity, likely from node2vec (optional)."""

    community_ids: Optional[List[str]] = None
    """The community IDs of the entity (optional)."""

    text_unit_ids: Optional[List[str]] = None
    """List of text unit IDs in which the entity appears (optional)."""

    document_ids: Optional[List[str]] = None
    """List of document IDs in which the entity appears (optional)."""

    rank: int = 1
    """
    Rank of the entity, used for sorting (optional). Higher rank indicates more important 
    entity. This can be based on centrality or other metrics.
    """

    attributes: Optional[Dict[str, Any]] = None
    """
    Additional attributes associated with the entity (optional), e.g. start time, end 
    time, etc. To be included in the search prompt.
    """
