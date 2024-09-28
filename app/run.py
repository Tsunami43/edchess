import os
from dotenv import load_dotenv

load_dotenv()
from .telegram.session import Session
from .stream import StreamClient
from .utils.proxy import Proxy
from . import handlers

proxy = Proxy()


async def start_execute():
    # Запуск клиента
    session = Session("mriya21")
    init_data = await session.get_tg_web_data()

    user_agent = "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"

    stream_client = StreamClient(
        user_agent=user_agent,  # proxy="http://localhost:1080"
    )
    stream_client.include_router(handlers.router)
    # Подключение к Каналу
    await stream_client.connect(init_data)
