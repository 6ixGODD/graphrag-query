# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

from . import _text as text
from ._text import (
    chunk_text,
    combine_embeddings,
    num_tokens,
)
from ._utils import (
    deserialize_json,
    filter_kwargs,
)

__all__ = [
    "text",
    "deserialize_json",
    "filter_kwargs",
    "chunk_text",
    "combine_embeddings",
    "num_tokens",
]
