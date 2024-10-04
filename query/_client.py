from os import PathLike
from pathlib import Path
from typing import Self, TypeVar, Union

from pydantic import BaseModel

Config_T = TypeVar("Config_T", bound=BaseModel)


class GraphRAGClient:
    @classmethod
    def from_config(cls, config: Union[Config_T, PathLike[str], Path, str]) -> Self: ...

    def __init__(
        self,
        *,
        context_dir: Union[str, PathLike[str], Path],
    ): ...


class AsyncGraphRAGClient:
    def __init__(self): ...
