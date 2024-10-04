# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from typing import Any, Dict, List, Optional

from ..._search._model._identified import Identified


class TextUnit(Identified):
    """A protocol for a TextUnit item in a Document database."""

    text: str = ""
    """The text of the unit."""

    text_embedding: Optional[List[float]] = None
    """The text embedding for the text unit (optional)."""

    entity_ids: Optional[List[str]] = None
    """List of entity IDs related to the text unit (optional)."""

    relationship_ids: Optional[List[str]] = None
    """List of relationship IDs related to the text unit (optional)."""

    covariate_ids: Optional[Dict[str, List[str]]] = None
    """Dictionary of different types of covariates related to the text unit (optional)."""

    n_tokens: Optional[int] = None
    """The number of tokens in the text (optional)."""

    document_ids: Optional[List[str]] = None
    """List of document IDs in which the text unit appears (optional)."""

    attributes: Optional[Dict[str, Any]] = None
    """A dictionary of additional attributes associated with the text unit (optional)."""
