from loguru import logger
from ..stream import Router, State, StreamClient, Message

router = Router()


@router.message("subscribe", state="game")
async def handle_subscribe(client: StreamClient, state: State, game: Game):
    await client.ping.start()
    if :
        move = 
        await client.send_message(
            {
                "rpc": {
                    "method": "move_proposal",
                    "data": {
                        "move": move,
                        "channel": game["channel"],
                        "ping": 247,
                        "last_seq_number": 0,
                        "time_left": 86378,
                        "is_web": True,
                    },
                },
            }
        )


@router.message("unsubscribe", state="game")
async def handle_unsubscribe(message: Message):
    logger.info(f"Unsubscribed from channel: {message}")


@router.message("push", state="game")
async def handle_push(message: Message):
    logger.info(f"Push received: {message}")


@router.message("rpc", state="game")
async def handle_rpc(message: Message):
    logger.info(f"Received RPC message: {message}")
