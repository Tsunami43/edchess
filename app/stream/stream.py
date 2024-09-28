import json
import aiohttp
from loguru import logger
from fake_useragent import UserAgent
from .base import Stream
from ..utils import Proxy
from .router import Router
from typing import Optional


class StreamClient(Stream):
    def __init__(
        self,
        url: str = "wss://prod-backend-core-oapiyfa2ga-el.a.run.app/ws/web",
        proxy: Optional[Proxy] = None,
        user_agent: Optional[str] = None,
    ):
        self.url = url
        self.proxy = proxy
        self.headers = {"User-Agent": user_agent or UserAgent().random}
        self.message_id: int = 0
        self.router = Router()
        self.__stream = None

    @property
    def __message_id(self) -> int:
        self.message_id += 1
        return self.message_id

    async def connect(self, token: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.ws_connect(
                    self.url, headers=self.headers, proxy=self.proxy
                ) as ws:
                    logger.info("Connected to WebSocket")
                    self.__stream = ws
                    await self.send_message({"connect": {"token": token, "name": "js"}})
                    await self.listener()
            except Exception as e:
                logger.critical(f"Error occurred during WebSocket connection: {str(e)}")

    def include_router(self, router: Router):
        for message_type, handler in router.handlers.items():
            if message_type in self.router.handlers:
                logger.warning(
                    f"Handler for message type '{message_type}' already exists. Overwriting."
                )
            self.router.handlers[message_type] = handler

    async def listener(self):
        try:
            while True:
                msg = await self.__stream.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data == {}:
                        await self.send_message(data, index=False)
                    else:
                        logger.debug(f"Received message: {data}")
                        try:
                            message_type = [key for key in data if key != "id"][0]
                        except IndexError:
                            message_type = None
                        await self.router.handle(message_type, self, data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {msg.text}")
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.info("WebSocket connection closed by server")
                    break
        except Exception as e:
            logger.error(f"Error in listner: {str(e)}")

    async def send_message(self, data: dict, index: bool = True):
        try:
            if index:
                data["id"] = self.__message_id
            await self.__stream.send_str(json.dumps(data))
            logger.info(f"Sent message: {data}")
        except Exception as e:
            logger.error(f"Failed to send message: {data}, Error: {str(e)}")
