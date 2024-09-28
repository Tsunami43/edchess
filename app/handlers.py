from loguru import logger
from .stream import Router

router = Router()


@router.message("connect")
async def handle_connect(client, data):
    await client.send_message(
        {
            "subscribe": {"channel": "wait_game_5be4f772-6a64-4122-8949-844e7f1b2928"},
        }
    )


@router.message("subscribe")
async def handle_subscribe(client, data):
    logger.info(f"Subscribe received: {data}")


@router.message("error")
async def handle_error(client, data):
    logger.error(f"Error received: {data}")


@router.message("unsubscribe")
async def handle_unsubscribe(client, data):
    logger.info(f"Unsubscribed from channel: {data}")


@router.message("push")
async def handle_push(client, data):
    logger.info(f"Push received: {data}")


@router.message("rpc")
async def handle_rpc(client, data):
    logger.info(f"Received RPC message: {data}")
