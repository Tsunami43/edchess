from loguru import logger
from ..stream import Router

router = Router()


@router.message("connect")
async def handle_connect(client, data):
    await client.send_message(
        {
            "subscribe": {"channel": f"wait_game_{client.account_id}"},
        }
    )
    client.state = "find_game"


@router.message("error")
async def handle_error(client, data):
    logger.error(f"Error received: {data}")
