from __future__ import annotations

from typing import (
    Dict,
    List,
    Tuple,
    TypeAlias,
    Union,
)

import pandas as pd

Context_T: TypeAlias = Tuple[Union[str, List[str]], Dict[str, pd.DataFrame]]

SingleContext_T: TypeAlias = Tuple[str, Dict[str, pd.DataFrame]]
