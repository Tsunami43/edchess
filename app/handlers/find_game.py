from loguru import logger
from ..stream import Router, State, StreamClient, Message
from ..chess import Chess


router = Router()


@router.message("subscribe", state="find_game")
async def handle_subscribe(client: StreamClient, message: Message):
    logger.info(f"Subscribed from channel: {message}")
    await client.send_message(
        {
            "rpc": {
                "method": "find_game",
                "data": {
                    "type": "bot",
                    "variation": {"type": "fast_game"},
                    "bot": {"level": 1, "color": "b"},
                },
            },
        }
    )


@router.message("unsubscribe", state="find_game")
async def handle_unsubscribe(client: StreamClient, message: Message, state: State):
    logger.info(f"Subscribed from channel: {message}")
    await client.send_message({"subscribe": {"channel": game.channel}})
    state.set("game")


@router.message("push", state="find_game")
async def handle_push(client: StreamClient, message: Message, state: State):
    """Обрабатывает сообщение 'push'."""
    logger.info(f"Push received: {message}")

    channel = data.get("push", {}).get("channel")
    pub_data = data.get("push", {}).get("pub", {}).get("data")

    if channel and pub_data:
        # Проверяем, является ли это сообщением о найденной игре
        if pub_data.get("name") == "game_found":
            game_info = pub_data.get("data", {})
            opponent = game_info.get("opponent", {})
            game_id = game_info.get("game_id")
            color = game_info.get("color")
            fen = game_info.get("fen")
            opponent_nickname = opponent.get("nickname")
            opponent_rating = opponent.get("rating", {}).get("current")
            channel_name = game_info.get("channel_name")  # Извлекаем channel_name

            chess = Chess(color)
            chess.set_fen_position(fen)
            game = Game(
                chess=Chess(),
                color=color,

            # Сохраняем информацию об игре
            state.data(game=game)
            context.data(
                "game",
                {
                    "id": game_id,
                    "chess": chess,
                    "opponent_nickname": opponent_nickname,
                    "opponent_rating": opponent_rating,
                    "channel": channel_name,
                },
            )

            await client.send_message(
                {
                    "unsubscribe": {"channel": f"wait_game_{client.account_id}"},
                }
            )
        else:
            logger.warning("Push does not contain a game_found message.")
    else:
        logger.warning("Invalid push message format.")


@router.message("rpc", state="find_game")
async def handle_rpc(message: Message):
    logger.info(f"Received RPC message: {message}")
