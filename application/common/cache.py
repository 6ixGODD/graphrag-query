import datetime
import time
from typing import Any, Dict, Iterable, Tuple, MutableMapping


class Cache(MutableMapping[str, Any]):
    """
    Threading-unsafe in-memory cache with optional TTL support.

    Attributes:
        _cache (Dict[str, Tuple[Any, float, datetime.timedelta | None]]): The cache dictionary
            containing the cached values, timestamps, and TTLs.
    """

    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float, datetime.timedelta | None]] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __delitem__(self, key: str) -> None:
        self.delete(key)

    def __contains__(self, key: str) -> bool:
        return self.exists(key) and self.get(key) is not None

    def __len__(self) -> int:
        return self._cache.__len__()

    def __iter__(self) -> Iterable[str]:
        return self._cache.__iter__()

    def __repr__(self) -> str:
        return self._cache.__repr__()

    def __str__(self) -> str:
        return self._cache.__str__()

    def set(self, key: str, value: Any, ttl: datetime.timedelta | None = None) -> None:
        self._cache[key] = (value, time.time(), ttl)

    def get(self, key: str) -> Any:
        if key in self._cache:
            value, timestamp, ttl = self._cache[key]
            if ttl is None or time.time() - timestamp < ttl.total_seconds():
                return value
            else:
                del self._cache[key]

    def getdel(self, key: str) -> Any:
        value = self.get(key)
        if value is not None:
            del self._cache[key]
        return value

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()

    def clear_expired(self) -> None:
        self._cache = {
            k: v for k, v in self._cache.items() if v[2] is None or time.time() - v[1] < v[2].total_seconds()
        }

    def exists(self, key: str) -> bool:
        return key in self._cache

    def expire(self, key: str, ttl: datetime.timedelta) -> None:
        if key in self._cache:
            value, timestamp, _ = self._cache[key]
            self._cache[key] = (value, timestamp, ttl)
        else:
            raise KeyError(f"Key '{key}' does not exist in the cache.")

    def incr(self, key: str) -> int:
        if key in self._cache:
            value, _, _ = self._cache[key]
            if not isinstance(value, int):
                raise ValueError("Value is not an integer.")
            value += 1
            self._cache[key] = (value, time.time(), None)
            return value
        else:
            self._cache[key] = (1, time.time(), None)
            return 1
