from typing import Callable, Dict, Any
from loguru import logger
import inspect
from .state import State


class Router:
    def __init__(self):
        self.state = State()
        self.handlers: Dict[str, Dict[str, Callable[..., Any]]] = {}

    def message(self, message_type: str, state: str = "*") -> Callable:
        """Декоратор для регистрации обработчика с учетом состояния."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if message_type not in self.handlers:
                self.handlers[message_type] = {}
            self.handlers[message_type][state] = func
            return func

        return decorator

    async def handle(self, client, message) -> None:
        """Обрабатывает сообщение на основе его типа и текущего состояния."""
        state_handlers = self.handlers.get(message.type, {})
        state = self.state.get()
        # Сначала пытаемся найти хэндлер для текущего состояния
        handler = state_handlers.get(state)

        if handler:
            logger.debug(
                f"Handler found for message type '{message.type}' and state '{state}'"
            )
            await self._call_handler(handler, client, message)
        else:
            # Если хэндлер для текущего состояния не найден, ищем хэндлер с состоянием '*'
            handler = state_handlers.get("*")
            if handler:
                logger.debug(
                    f"Handler found for message type '{message.type}' with universal state '*'"
                )
                await self._call_handler(handler, client, message)
            else:
                logger.warning(f"Unknown message type: {message.type} | State: {state}")

    async def _call_handler(self, handler: Callable[..., Any], client, message) -> None:
        """Вызывает хэндлер, передавая ему только нужные параметры."""
        # Получаем сигнатуру хэндлера
        sig = inspect.signature(handler)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name == "client":
                kwargs[param_name] = client
            elif param_name == "message":
                kwargs[param_name] = message
            elif param_name == "state":
                kwargs[param_name] = self.state
            elif param_name in self.state.data:
                kwargs[param_name] = self.state.data[param_name]

        # Вызываем хэндлер с переданными аргументами
        try:
            await handler(**kwargs)
        except Exception as e:
            logger.error(e)
