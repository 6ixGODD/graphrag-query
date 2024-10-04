from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Self, TypeVar, Union

from pydantic import BaseModel

Config_T = TypeVar("Config_T", bound=BaseModel)

__all__ = [
    'GraphRAGClient',
    'AsyncGraphRAGClient',
]


class GraphRAGClient:
    @classmethod
    def from_config(cls, config: Union[Config_T, PathLike[str], Path, str]) -> Self: ...

    def __init__(
        self,
        *,
        context_dir: Union[str, PathLike[str], Path],
    ): ...


class AsyncGraphRAGClient:
    @classmethod
    def from_config(cls, config: Union[Config_T, PathLike[str], Path, str]) -> Self: ...

    def __init__(self): ...
