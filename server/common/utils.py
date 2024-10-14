# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing
import uuid


def gen_id(prefix: typing.Optional[str] = None, *, split: str = '-') -> str:
    """Generate a random ID with the given prefix (optional)."""
    return f"{prefix}{split}{uuid.uuid4().hex}" if prefix else uuid.uuid4().hex
