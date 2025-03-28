from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def create_user(self):
        raise NotImplementedError

    @abstractmethod
    async def get_users(self):
        raise NotImplementedError
