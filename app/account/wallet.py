import aiohttp
from typing import Optional
from loguru import logger


async def fetch_balance(user_agent: str, telegram_query: str) -> Optional[float]:
    url = "https://prod-backend-auth-oapiyfa2ga-el.a.run.app/wallets"

    # Ваши кастомные заголовки
    headers = {
        "User-Agent": user_agent,  # Задаем свой User-Agent
        "telegram-query": telegram_query,  # Задаем свой telegram-query
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "cache-control": "no-cache",
        "edchess-version": "1.0.10",
        "origin": "https://telegram.edchess.io",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://telegram.edchess.io/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                # Проверяем статус ответа
                if response.status == 200:
                    wallets_data = await response.json()  # Декодируем JSON-ответ
                    balance = wallets_data[0].get("balance")  # Получаем ID
                    return balance  # Возвращаем ID
                else:
                    logger.error(
                        f"Error: {response.status}, Message: {await response.text()}"
                    )
                    return None

        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
