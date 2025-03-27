from abc import ABC, abstractmethod
from typing import Any


class ICache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Get value from cache by key"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = None) -> None:
        """Set value in cache with optional expiration in seconds"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache by key"""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache"""
        pass

    @abstractmethod
    async def get_all_keys(self) -> list[str]:
        """Get all keys in cache"""
        pass

    @abstractmethod
    async def get_all_values(self) -> list[Any]:
        """Get all values in cache"""
        pass
