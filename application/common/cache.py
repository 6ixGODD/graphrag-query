# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import datetime
import time
import typing

import typing_extensions


class Cache(typing.MutableMapping[str, typing.Any]):
    """
    Threading-unsafe in-memory cache with optional TTL support.

    Attributes:
        _cache (typing.Dict[str, typing.Tuple[typing.Any, float, typing.Optional[datetime.timedelta]]]):
            The cache dictionary containing the cached values, timestamps, and TTLs.
    """

    def __init__(self) -> None:
        self._cache: typing.Dict[str, typing.Tuple[typing.Any, float, typing.Optional[datetime.timedelta]]] = {}

    @typing_extensions.override
    def __setitem__(self, key: str, value: typing.Any) -> None:
        self.set(key, value)

    @typing_extensions.override
    def __getitem__(self, key: str) -> typing.Any:
        return self.get(key)

    @typing_extensions.override
    def __delitem__(self, key: str) -> None:
        self.delete(key)

    @typing_extensions.override
    def __contains__(self, key: object) -> bool:
        return self.exists(key.__str__()) and self.get(key.__str__()) is not None

    @typing_extensions.override
    def __len__(self) -> int:
        return self._cache.__len__()

    @typing_extensions.override
    def __iter__(self) -> typing.Iterator[str]:
        return self._cache.__iter__()

    @typing_extensions.override
    def __repr__(self) -> str:
        return self._cache.__repr__()

    @typing_extensions.override
    def __str__(self) -> str:
        return self._cache.__str__()

    def set(self, key: str, value: typing.Any, ttl: typing.Optional[datetime.timedelta] = None) -> None:
        self._cache[key] = (value, time.time(), ttl)

    @typing_extensions.override
    def get(self, key: str, default: typing.Optional[typing.Any] = None) -> typing.Any:
        if key in self._cache:
            value, timestamp, ttl = self._cache[key]
            if ttl is None or time.time() - timestamp < ttl.total_seconds():
                return value
            else:
                del self._cache[key]
        return default

    def getdel(self, key: str) -> typing.Any:
        value = self.get(key)
        if value is not None:
            del self._cache[key]
        return value

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    @typing_extensions.override
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
