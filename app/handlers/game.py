from loguru import logger
from ..stream import Router

router = Router()


@router.message("subscribe", state="game")
async def handle_subscribe(client, data, context):
    logger.info(f"Subscribe received: {data}")


@router.message("unsubscribe", state="game")
async def handle_unsubscribe(client, data, context):
    logger.info(f"Unsubscribed from channel: {data}")


@router.message("push", state="game")
async def handle_push(client, data, context):
    logger.info(f"Push received: {data}")


@router.message("rpc", state="game")
async def handle_rpc(client, data, context):
    logger.info(f"Received RPC message: {data}")
