import asyncio
import random
from loguru import logger
from ..stream import Router, State, StreamClient, Message
from ..game import Game

router = Router()


@router.message("subscribe", state="game")
async def handle_subscribe(client: StreamClient, game: Game):
    await client.ping.start(client)
    if game.get_turn() == game.color:
        game.timer.start()
        await asyncio.sleep(1 + round(random.uniform(0.1, 0.5), 2))
        await client.send_message(
            {
                "rpc": {
                    "method": "move_proposal",
                    "data": {
                        "move": game.get_move(),
                        "channel": game.channel,
                        "ping": client.ping.prev_ping,
                        "last_seq_number": 0,
                        "time_left": game.timer.stop(),
                        "is_web": True,
                    },
                },
            }
        )


@router.message("unsubscribe", state="game")
async def handle_unsubscribe(client: StreamClient, state: State):
    client.ping.stop()
    state.clear()
    await client.disconnect()


@router.message("push", state="game")
async def handle_push(client: StreamClient, message: Message, state: State, game: Game):
    """
    Обрабатывает сообщения о ходе и завершении игры.

    :param client: Экземпляр клиента.
    :param message: Сообщение с данными о ходе или завершении игры.
    :param state: Состояние игры.
    :param game: Объект текущей игры.
    """
    push_data = message.data
    channel = push_data.get("channel")
    pub_data = push_data.get("pub", {}).get("data")

    if channel and pub_data and channel == game.channel:
        name = pub_data.get("name")

        if name == "new_move":
            move_data = pub_data.get("data", {})
            if "finished" in move_data:
                finished_data = move_data.get("finished", {})
                reason = finished_data.get("reason", "")
                win_color = finished_data.get("win_color", "")
                logger.info(
                    f"Game finished: {reason}, Winner: {win_color}\n"
                    f"I - {game.color}\n"
                    f"{game.oponent}"
                )
                await client.send_message(
                    {
                        "unsubscribe": {"channel": game.channel},
                    }
                )
            else:
                move_data = pub_data.get("data", {})
                move = move_data.get("move", "")
                fen = move_data.get("fen", "")
                logger.info(f"New move received: {move}, FEN: {fen}")
                game.fen = fen
                if game.get_turn() == game.color:
                    game.timer.start()
                    last_seq_number: int = move_data.get("seq_number")
                    await asyncio.sleep(
                        round(random.uniform(1, 1 + 0.1 * last_seq_number), 4)
                    )
                    await client.send_message(
                        {
                            "rpc": {
                                "method": "move_proposal",
                                "data": {
                                    "move": game.get_move(),
                                    "channel": game.channel,
                                    "ping": client.ping.prev_ping,
                                    "last_seq_number": last_seq_number,
                                    "time_left": game.timer.stop(),
                                    "is_web": True,
                                },
                            },
                        }
                    )
                state.set_data("game", game)
        elif name == "stop_timer":
            sn = pub_data.get("data", {}).get("sn")
            logger.info(f"Timer stopped for sequence number: {sn}")

        else:
            logger.warning(f"Unknown message type: {name}")
    else:
        logger.warning(f"Invalid message: {message}")


@router.message("rpc", state="game")
async def handle_rpc(message: Message):
    logger.info(f"Received RPC message: {message}")
