import json
import aiohttp
import time
from typing import Optional
from loguru import logger
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from .base import Stream
from .router import Router
from .ping import PingClient
from .message import Message


class StreamClient(Stream):
    def __init__(
        self,
        account_id: str,
        init_data: str,
        url: str = "wss://prod-backend-core-oapiyfa2ga-el.a.run.app/ws/web",
        proxy_url: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        self.account_id = account_id
        self.token = init_data
        self.url = url
        self.headers = {"User-Agent": user_agent or UserAgent().random}
        self.message_id: int = 0
        self.router = Router()
        self.ping = PingClient()
        self.__websocket = None
        self.proxy = proxy_url

    @property
    def __message_id(self) -> int:
        self.message_id += 1
        return self.message_id

    async def connect(self):
        async with aiohttp.ClientSession(
            connector=ProxyConnector.from_url(self.proxy)
        ) as session:
            try:
                async with session.ws_connect(self.url, headers=self.headers) as ws:
                    logger.info("Connected to WebSocket")
                    self.__websocket = ws
                    await self.send_message(
                        {"connect": {"token": self.token, "name": "js"}}
                    )
                    await self.listener()
            except Exception as e:
                logger.critical(f"Error occurred during WebSocket connection: {str(e)}")

    def include_router(self, router: Router):
        """Включает роутер в клиент, добавляя его хэндлеры."""
        for message_type, state_handlers in router.handlers.items():
            for state, handler in state_handlers.items():
                # Добавляем хэндлер в основной роутер
                if message_type not in self.router.handlers:
                    self.router.handlers[message_type] = {}
                self.router.handlers[message_type][state] = handler

    async def listener(self):
        try:
            while self.__websocket is not None:
                msg = await self.__websocket.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data == {}:
                        state = self.router.state.get()
                        state_data = self.router.state.data.get("find_game", None)
                        if state == "find_game" and state_data:
                            if int(time.time() - state_data) > 30:
                                await self.disconnect()
                        else:
                            await self.send_message(data, index=False)
                    else:
                        await self.router.handle(self, Message(data))
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {msg.text}")
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.info("WebSocket connection closed by server")
                    break
        except Exception as e:
            logger.error(f"Error in listner: {e}")

    async def send_message(self, data: dict, index: bool = True):
        try:
            if index:
                data["id"] = self.__message_id
            await self.__websocket.send_str(json.dumps(data))
            logger.info(f"Sent message: {data}")
        except Exception as e:
            logger.error(f"Failed to send message: {data}, Error: {str(e)}")

    async def disconnect(self):
        self.ping.stop()
        if self.__websocket:
            await self.__websocket.close()
            self.__websocket = None
            logger.info("WebSocket disconnected.")
