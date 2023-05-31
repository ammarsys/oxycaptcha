"""TTL Cache implementation for the Flask API"""

import datetime
from typing import Generic, TypeVar, Hashable, Generator, Optional, overload, Union
from collections.abc import MutableMapping


KT = TypeVar("KT", bound=Hashable)
VT = TypeVar("VT")
T = TypeVar("T")


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

        self.__check_expiry()
        return self.cache[item][0]

    def __contains__(self, item) -> bool:
        self.__check_expiry()

        try:
            _, dt = self.cache[item]

            if not _check_if_expired(dt):
                return True
        except KeyError:
            return False

        del self.cache[item]
        return False

    def __setitem__(self, key: KT, value: VT) -> None:
        self.__check_expiry()

        self.cache[key] = (value, _time(self.ttl))

    def __len__(self) -> int:
        return len(self.cache)

    def __iter__(self) -> Generator:
        yield from self.cache

    def __delitem__(self, key: KT) -> None:
        del self.cache[key]

    def __str__(self) -> str:
        return str(self.cache)

    @overload
    def get(self, item: KT, /) -> Optional[VT]:
        ...

    @overload
    def get(self, item: KT, /, default: T) -> Union[VT, T]:  # noqa
        ...

    def get(self, item: KT, /, default: Optional[T] = None) -> Union[VT, T, None]:
        self.__check_expiry()

        return self.cache.get(item, (default,))[0]

    def __check_expiry(self) -> None:
        """This function removes expired records from the cache dictionary.

        We can loop through the dictionary items in a reverse order and delete any expired key-value pairs.
        The moment we find a non-expired key-value pair in said loop, we break out because it is guaranteed that any
        object after it is not expired (since dictionaries are ordered since Python 3.7, this means that the newest
        key ([0]) is the newest by time  and the oldest ([-1]) is the oldest)

        This function is to be called in (almost) all dunder methods.
        """

        for key, value in reversed(list(self.cache.items())):
            if not _check_if_expired(value[1]):
                break

            print("Removing", key, value, " because its expired")
            self.cache.pop(key)
