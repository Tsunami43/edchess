import asyncio
from typing import Optional
from urllib.parse import unquote
from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered,
    FloodWait,
    Unauthorized,
    UserDeactivated,
)
from pyrogram.raw.functions.messages import RequestWebView
from loguru import logger
from .exceptions import InvalidSession
from ..utils.proxy import Proxy


class Session:
    def __init__(
        self,
        name: str,
        api_id: Optional[int] = None,
        api_hash: Optional[str] = None,
        proxy: Optional[Proxy] = None,
    ):
        self.name = name
        self.client = Client(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            proxy=proxy.data if proxy else proxy,
            workdir="sessions",
        )

    async def get_tg_web_data(self) -> str:
        try:
            if not self.client.is_connected:
                try:
                    await self.client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.client.name)

            dialogs = self.client.get_dialogs()
            async for dialog in dialogs:
                if (
                    dialog.chat
                    and dialog.chat.username
                    and dialog.chat.username == "hamster_kombat_bot"
                ):
                    break

            while True:
                try:
                    peer = await self.client.resolve_peer("edchess_bot")
                    break
                except FloodWait as fl:
                    fls = fl.value
                    logger.warning(f"{self.name} | FloodWait {fl}")
                    fls *= 2
                    logger.info(f"{self.name} | Sleep {fls}s")

                    await asyncio.sleep(fls)

            web_view = await self.client.invoke(
                RequestWebView(
                    peer=peer,
                    bot=peer,
                    platform="android",
                    from_bot_menu=False,
                    url="https://telegram.edchess.io/",
                )
            )

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split("tgWebAppData=", maxsplit=1)[1].split(
                    "&tgWebAppVersion", maxsplit=1
                )[0]
            )

            if self.client.is_connected:
                await self.client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(
                f"{self.name} | Unknown error while getting Tg Web Data: {error}"
            )
            await asyncio.sleep(delay=3)