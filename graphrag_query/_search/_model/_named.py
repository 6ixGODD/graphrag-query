from __future__ import annotations

from . import _identified


class Named(_identified.Identified):
    """A protocol for an item with a name/title."""

    title: str = ""
    """The name/title of the item."""
