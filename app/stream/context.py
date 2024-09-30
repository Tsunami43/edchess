from typing import Dict, Any
from loguru import logger


class Context:
    def __init__(self, state: str = "*", data: Dict[str, Any] = None):
        """
        Класс для управления состоянием и данными.

        :param state: Текущее состояние.
        :param data: Дополнительные данные, которые можно сохранять в состоянии.
        """
        self.__state = state
        self.__data = data or {}

    @property
    def state(self) -> str:
        """Возвращает текущее состояние."""
        return self.__state

    @state.setter
    def state(self, new_state: str) -> None:
        """Устанавливает новое состояние."""
        logger.debug(f"Смена состояния с {self.__state} на {new_state}")
        self.__state = new_state

    @property
    def data(self) -> Dict[str, Any]:
        """Возвращает все данные."""
        return self.__data

    @data.setter
    def data(self, key: str, value: Any) -> None:
        """Устанавливает данные в состоянии."""
        self.__data[key] = value

    def clear_data(self) -> None:
        """Очищает все данные."""
        self.__data.clear()
