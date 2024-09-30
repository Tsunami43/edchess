import json


class DataWrapper:
    """Класс для хранения данных, чтобы обращаться через data.token, data.name и т.д."""

    def __init__(self, data: dict):
        # Устанавливаем данные как атрибуты объекта
        for key, value in data.items():
            if isinstance(value, dict):
                # Если значение — словарь, создаем вложенный объект DataWrapper
                setattr(self, key, DataWrapper(value))
            else:
                # Иначе просто присваиваем значение
                setattr(self, key, value)

    def __repr__(self):
        return f"DataWrapper({self.__dict__})"


class Message:
    def __init__(self, data: dict):
        # Извлекаем id на верхнем уровне
        self.id = data.get("id")
        # Определяем тип (основной ключ, кроме id)
        self.type = self._extract_type(data)
        # Данные типа сохраняем в объект DataWrapper
        if self.type in data:
            self.data = DataWrapper(data[self.type])
        else:
            self.data = None

    def _extract_type(self, data: dict) -> str:
        """Получаем тип сообщения, исключая 'id'."""
        for key in data:
            if key != "id":
                return key
        return None

    def __repr__(self):
        return f"Message(id={self.id}, type='{self.type}', data={self.data})"
