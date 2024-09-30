from loguru import logger
from ..stream import Router

router = Router()


@router.message("subscribe", state="find_game")
async def handle_subscribe(client, data, context):
    logger.info(f"Subscribed from channel: {data}")
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
async def handle_unsubscribe(client, data, context):
    await client.send_message(
        {"subscribe": {"channel": context.data["game"]["channel"]}}
    )
    context.state = "game"


@router.message("push", state="find_game")
async def handle_push(client, data, context):
    """Обрабатывает сообщение 'push'."""
    logger.info(f"Push received: {data}")

    channel = data.get("push", {}).get("channel")
    pub_data = data.get("push", {}).get("pub", {}).get("data")

    if channel and pub_data:
        # Проверяем, является ли это сообщением о найденной игре
        if pub_data.get("name") == "game_found":
            game_info = pub_data.get("data", {})
            opponent = game_info.get("opponent", {})
            game_id = game_info.get("game_id")
            color = game_info.get("color")
            opponent_nickname = opponent.get("nickname")
            opponent_rating = opponent.get("rating", {}).get("current")
            channel_name = game_info.get("channel_name")  # Извлекаем channel_name

            # Сохраняем информацию об игре
            context.data(
                "game",
                {
                    "id": game_id,
                    "color": color,
                    "opponent_nickname": opponent_nickname,
                    "opponent_rating": opponent_rating,
                    "channel": channel_name,  # Добавляем channel_name
                },
            )

            logger.info(
                f"Game found! ID: {game_id}, Color: {color}, Opponent: {opponent_nickname}, Opponent Rating: {opponent_rating}, Channel Name: {channel_name}"
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
async def handle_rpc(client, data, context):
    logger.info(f"Received RPC message: {data}")
