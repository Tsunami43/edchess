from abc import ABC, abstractmethod


class Stream(ABC):
    @abstractmethod
    async def connect():
        raise NotImplementedError

    @abstractmethod
    async def listener():
        raise NotImplementedError

    @abstractmethod
    async def send_message():
        raise NotImplementedError
