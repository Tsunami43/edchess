import asyncio
import random
from typing import Optional
from loguru import logger
from .telegram.session import Session
from .stream import StreamClient
from .utils import Profile
from .handlers import master, game, find_game
from .account import Account


async def start_execute(name: str):
    profile = Profile(name)
    session = Session(name, proxy_data=profile.proxy_data)
    account = Account(profile.user_agent, profile.proxy_url)
    account_id: Optional[str] = None
    try:
        while True:
            init_data = await session.get_tg_web_data()

            balance = await account.fetch_balance(init_data)
            logger.info(f"Balance: {balance}")

            if account_id is None:
                account_id = await account.fetch_account_id(init_data)
                if account_id is None:
                    raise ValueError("`Account_id` is None")

            stream_client = StreamClient(
                init_data=init_data,
                account_id=account_id,
                user_agent=profile.user_agent,
                proxy_url=profile.proxy_url,
            )

            stream_client.include_router(master.router)
            stream_client.include_router(game.router)
            stream_client.include_router(find_game.router)

            await asyncio.sleep(random.randint(2, 4))
            await stream_client.connect()

            fsl = random.randint(30, 60)
            logger.info(f"Pause: {fsl}sec.")
            await asyncio.sleep(fsl)
    except Exception as e:
        logger.critical(e)
    finally:
        await account.close()
