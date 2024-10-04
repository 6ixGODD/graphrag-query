from typing import Any, Dict, List, Optional

from ..._search._model._named import Named


class CommunityReport(Named):
    """Defines an LLM-generated summary report of a community."""

    community_id: str
    """The ID of the community this report is associated with."""

    summary: str = ""
    """Summary of the report."""

    full_content: str = ""
    """Full content of the report."""

    rank: float = 1.0
    """Rank of the report, used for sorting (optional). Higher means more important"""

    summary_embedding: Optional[List[float]] = None
    """The semantic (i.e. text) embedding of the report summary (optional)."""

    full_content_embedding: Optional[List[float]] = None
    """The semantic (i.e. text) embedding of the full report content (optional)."""

    attributes: Optional[Dict[str, Any]] = None
    """A dictionary of additional attributes associated with the report (optional)."""
