from typing import Callable, Dict, Any
from loguru import logger
from .context import Context


class Router:
    def __init__(self):
        self.context = Context()
        self.handlers: Dict[str, Dict[str, Callable[..., Any]]] = {}

    def message(self, message_type: str, state: str = "*") -> Callable:
        """Декоратор для регистрации обработчика с учетом состояния."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if message_type not in self.handlers:
                self.handlers[message_type] = {}
            self.handlers[message_type][state] = func
            return func

        return decorator

    async def handle(self, message_type: str, *args) -> None:
        """Обрабатывает сообщение на основе его типа и текущего состояния."""
        state_handlers = self.handlers.get(message_type, {})

        # Сначала пытаемся найти хэндлер для текущего состояния
        handler = state_handlers.get(self.context.state)

        if handler:
            logger.debug(
                f"Handler found for message type '{message_type}' and state '{self.context.state}'"
            )
            await handler(*args, context=self.context)
        else:
            # Если хэндлер для текущего состояния не найден, ищем хэндлер с состоянием '*'
            handler = state_handlers.get("*")
            if handler:
                logger.debug(
                    f"Handler found for message type '{message_type}' with universal state '*'"
                )
                await handler(*args, context=self.context)
            else:
                logger.warning(
                    f"Unknown message type: {message_type} | State: {self.context.state} | Args: {args}"
                )
