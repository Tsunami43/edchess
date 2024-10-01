import os
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


async def start_execute():
    # Запуск клиента
    session = Session("mriya21")
    init_data = await session.get_tg_web_data()

    user_agent = "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"

    stream_client = StreamClient(
        account_id=await profile.fetch_account_id(user_agent, init_data),
        user_agent=user_agent,
    )
    stream_client.include_router(master.router)
    stream_client.include_router(game.router)
    stream_client.include_router(find_game.router)
    logger.info(f"Balance: {await wallet.fetch_balance(user_agent, init_data)}")
    # Подключение к Каналу
    await asyncio.sleep(random.randint(2, 4))
    while True:
        await stream_client.connect(init_data)
        fsl = random.randint(80, 120)
        logger.info(f"Pause: {fls}sec.")
        await asyncio.sleep(fls)
