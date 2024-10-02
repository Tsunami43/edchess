import asyncio
import random
from loguru import logger
from dotenv import load_dotenv
from .telegram.session import Session
from .stream import StreamClient
from .utils.proxy import Proxy
from .handlers import master, game, find_game
from .account import profile, wallet

load_dotenv()
proxy = Proxy()
session = Session("mriya21", proxy=proxy)
user_agent = "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"


async def start_execute():
    while True:
        init_data = await session.get_tg_web_data()
        logger.info(
            f"Balance: {await wallet.fetch_balance(user_agent, init_data, proxy_url=proxy.url)}"
        )
        stream_client = StreamClient(
            account_id=await profile.fetch_account_id(
                user_agent=user_agent,
                telegram_query=init_data,
                proxy_url=proxy.url,
            ),
            user_agent=user_agent,
            proxy_url=proxy.url,
        )
        stream_client.include_router(master.router)
        stream_client.include_router(game.router)
        stream_client.include_router(find_game.router)
        # Подключение к Каналу

        await asyncio.sleep(random.randint(2, 4))
        await stream_client.connect(init_data)
        fsl = random.randint(120, 180)
        logger.info(f"Pause: {fsl}sec.")
        await asyncio.sleep(fsl)
