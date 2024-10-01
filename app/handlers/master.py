from loguru import logger
from ..stream import Router, State, StreamClient, Message

router = Router()


@router.message("connect")
async def handle_connect(message: Message, client: StreamClient, state: State):
    logger.info(f"{message}")
    await client.send_message(
        {
            "subscribe": {"channel": f"wait_game_{client.account_id}"},
        }
    )
    state.set("find_game")


@router.message("error")
async def handle_error(message: Message):
    logger.error(f"Error received: {message}")
