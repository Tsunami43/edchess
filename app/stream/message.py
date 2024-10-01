import json


class Message:
    def __init__(self, data: dict):
        # Извлекаем id на верхнем уровне
        self.id = data.get("id")
        # Определяем тип (основной ключ, кроме id)
        self.type = self._extract_type(data)
        # Сохраняем остальные данные в формате JSON
        self.data = data[self.type] if self.type else {}

    def _extract_type(self, data: dict) -> str:
        """Получаем тип сообщения, исключая 'id'."""
        for key in data:
            if key != "id":
                return key
        return None

    def __repr__(self):
        return f"Message(id={self.id}, type='{self.type}', data={self.get_data()})"
