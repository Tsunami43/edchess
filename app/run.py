import os
from dotenv import load_dotenv

load_dotenv()
from .telegram.session import Session
from .stream import StreamClient
from .utils.proxy import Proxy
from .handlers import master, game, find_game
from .account import profile

proxy = Proxy()


async def start_execute():
    # Запуск клиента
    session = Session("mriya21")
    init_data = await session.get_tg_web_data()

    user_agent = "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"

    stream_client = StreamClient(
        account_id="5be4f772-6a64-4122-8949-844e7f1b2928",  # await profile.fetch_account_id(user_agent, init_data),
        user_agent=user_agent,  # proxy="http://localhost:1080"
    )
    stream_client.include_router(master.router)
    stream_client.include_router(game.router)
    stream_client.include_router(find_game.router)
    # Подключение к Каналу
    await stream_client.connect(init_data)
