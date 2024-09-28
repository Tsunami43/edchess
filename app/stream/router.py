from typing import Callable, Dict, Any
from loguru import logger


class Router:
    def __init__(self):
        self.handlers: Dict[str, Callable[..., Any]] = {}

    def message(self, message_type: str) -> Callable:
        """Декоратор для регистрации обработчика."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.handlers[message_type] = func
            return func

        return decorator

    async def handle(self, message_type: str, *args, **kwargs) -> None:
        """Обрабатывает сообщение на основе его типа."""
        handler = self.handlers.get(message_type)

        if handler:
            await handler(*args, **kwargs)
            logger.debug(f"Get message type: {message_type}")
        else:
            logger.warning(f"Unknown message type: {message_type} | {args}")
