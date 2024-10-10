from loguru import logger
from ..stream import Router, State, StreamClient, Message
import time

router = Router()


@router.message("connect")
async def handle_connect(client: StreamClient, state: State):
    await client.send_message(
        {
            "subscribe": {"channel": f"wait_game_{client.account_id}"},
        }
    )
    state.set("find_game")
    state.set_data("find_game", time.time())


@router.message("error")
async def handle_error(message: Message):
    logger.error(f"Error received: {message}")
