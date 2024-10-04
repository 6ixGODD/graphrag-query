from __future__ import annotations

from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import (
    Any,
    Self,
    Union,
)

from ...._search._context import _builders


class BaseContextLoader(ABC):
    @classmethod
    @abstractmethod
    def from_parquet_directory(cls, directory: Union[PathLike[str], Path], **kwargs: str) -> Self: ...

    @abstractmethod
    def to_context_builder(self, *args, **kwargs: Any) -> _builders.BaseContextBuilder: ...
