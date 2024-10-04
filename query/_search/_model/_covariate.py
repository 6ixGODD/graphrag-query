# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..._search._model._identified import Identified


class Covariate(Identified):
    """
    A protocol for a covariate in the system.

    Covariates are metadata associated with a subject, e.g. entity claims.
    Each subject (e.g. entity) may be associated with multiple types of covariates.
    """

    subject_id: str = ""
    """The subject id."""

    subject_type: str = "entity"
    """The subject type."""

    covariate_type: str = "claim"
    """The covariate type."""

    text_unit_ids: Optional[List[str]] = None
    """List of text unit IDs in which the covariate info appears (optional)."""

    document_ids: Optional[List[str]] = None
    """List of document IDs in which the covariate info appears (optional)."""

    attributes: Optional[Dict[str, Any]] = None
