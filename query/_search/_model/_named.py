# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from ..._search._model._identified import Identified


class Named(Identified):
    """A protocol for an item with a name/title."""

    title: str = ""
    """The name/title of the item."""
