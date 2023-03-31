"""TTL Cache implementation for the Flask API"""

import datetime
from typing import (
    Generic,
    TypeVar,
    Hashable,
    Generator,
)
from collections.abc import MutableMapping


KT = TypeVar("KT", bound=Hashable)
VT = TypeVar("VT")


def _check_if_expired(item: datetime.datetime) -> bool:
    """Check if a record has expired"""
    return item <= datetime.datetime.now()


def _time(seconds: int) -> datetime.datetime:
    """Make a timedelta in the future"""
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


class TTLCache(MutableMapping[KT, VT], Generic[KT, VT]):
    """
    TTL (time-to-live) cache for pyaww module. This class is utilised inside pyaww.utils.Cache. Records may expire
    upon interacting with them (__getitem__ and __contains__.)

    Ordinary format for the cache instance variable is the submodule initialized class id and the initialized class.

    """

    def __init__(self, ttl: int = 30):
        self.ttl = ttl
        self.cache: dict[KT, tuple[VT, datetime.datetime]] = {}

    def __getitem__(self, item: KT) -> VT:
        if item not in self:
            raise KeyError

        return self.cache[item][0]

    def __contains__(self, item) -> bool:
        try:
            _, dt = self.cache[item]

            if not _check_if_expired(dt):
                return True
        except KeyError:
            return False

        del self.cache[item]
        return False

    def __setitem__(self, key: KT, value: VT) -> None:
        self.cache[key] = (value, _time(self.ttl))

    def __len__(self) -> int:
        return len(self.cache)

    def __iter__(self) -> Generator:
        yield from self.cache

    def __delitem__(self, key: KT) -> None:
        del self.cache[key]

    def __str__(self) -> str:
        return str(self.cache)

    def get(self, item: KT) -> VT:
        return self.cache.get(item)[0]
