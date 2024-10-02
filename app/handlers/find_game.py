import asyncio
from loguru import logger
from ..stream import Router, State, StreamClient, Message
from ..game import Game


router = Router()


@router.message("subscribe", state="find_game")
async def handle_subscribe(client: StreamClient):
    await client.send_message(
        {
            "rpc": {
                "method": "find_game",
                "data": {
                    "type": "comp",
                    "variation": {"type": "blitz"},
                    "comp": {"amount": "0.1", "net": "ton"},
                },
            },
        }
    )
    # await client.send_message(
    #     {
    #         "rpc": {
    #             "method": "find_game",
    #             "data": {
    #                 "type": "bot",
    #                 "variation": {"type": "fast_game"},
    #                 "bot": {"level": 1, "color": "b"},
    #             },
    #         },
    #     }
    # )


@router.message("unsubscribe", state="find_game")
async def handle_unsubscribe(client: StreamClient, state: State, game: Game):
    if game.oponent.nickname == "Daddy" and game.color == "b":
        await asyncio.sleep(209)
        state.clear()
        await client.disconnect()
    else:
        await client.send_message({"subscribe": {"channel": game.channel}})
        state.set("game")


@router.message("push", state="find_game")
async def handle_push(client: StreamClient, message: Message, state: State):
    """Обрабатывает сообщение 'push'."""
    channel = message.data.get("channel")
    pub_data = message.data.get("pub", {}).get("data")
    if channel and pub_data:
        # Проверяем, является ли это сообщением о найденной игре
        if pub_data.get("name") == "game_found":
            game_info = pub_data.get("data", {})
            oponent = game_info.get("opponent", {})
            game = Game(
                id=game_info.get("game_id"),
                fen=game_info.get("fen"),
                color=game_info.get("color"),
                oponent_nickname=oponent.get("nickname"),
                oponent_rating=oponent.get("rating", {}).get("current"),
                channel=game_info.get("channel_name"),
                timers=game_info.get("timers", {}),
            )

            # Сохраняем информацию об игре
            state.set_data("game", game)
            await client.send_message(
                {
                    "unsubscribe": {"channel": f"wait_game_{client.account_id}"},
                }
            )
            # else:
            #     logger.warning(f"Your oponent: {opponent.get('nickname')}")
        else:
            logger.warning("Push does not contain a game_found message.")
    else:
        logger.warning("Invalid push message format.")


@router.message("rpc", state="find_game")
async def handle_rpc(message: Message):
    logger.info(f"Received RPC message: {message}")
