from loguru import logger
from ..stream import Router, Context

router = Router()


@router.message("connect")
async def handle_connect(client, data, context):
    await client.send_message(
        {
            "subscribe": {"channel": f"wait_game_{client.account_id}"},
        }
    )
    context.state = "find_game"


@router.message("error")
async def handle_error(client, data, context):
    logger.error(f"Error received: {data}")
