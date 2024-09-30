from typing import Dict, Any
from loguru import logger


class State:
    def __init__(self, state: str = "*", data: Dict[str, Any] = None):
        self.__state: str = state
        self.__data: Dict[str, Any] = data or {}

    def get(self) -> str:
        return self.__state

    def set(self, new_state: str) -> None:
        self.__state = new_state

    @property
    def data(self) -> Dict[str, Any]:
        """Возвращает все данные."""
        return self.__data

    @data.setter
    def data(self, **kwargs) -> None:
        """Устанавливает данные в состоянии."""
        for key, value in kwargs.items():
            self.__data[key] = value

    def clear_data(self) -> None:
        """Очищает все данные."""
        self.__data.clear()