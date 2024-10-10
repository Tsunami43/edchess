import aiohttp
from typing import Optional
from loguru import logger
from aiohttp_socks import ProxyConnector


class Account:
    def __init__(
        self,
        user_agent: Optional[str] = None,
        proxy_url: Optional[str] = None,
    ):
        self.user_agent = user_agent
        self.connector = ProxyConnector.from_url(proxy_url) if proxy_url else None
        self.session = aiohttp.ClientSession(connector=self.connector)

    def headers(self, telegram_query: str):
        return {
            "User-Agent": self.user_agent,
            "telegram-query": telegram_query,
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

    async def fetch_balance(self, telegram_query: str) -> Optional[float]:
        url = "https://prod-backend-auth-oapiyfa2ga-el.a.run.app/wallets"
        try:
            async with self.session.get(
                url, headers=self.headers(telegram_query)
            ) as response:
                if response.status == 200:
                    wallets_data = await response.json()
                    balance = wallets_data[0].get("balance")
                    return balance
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

    async def fetch_account_id(self, telegram_query: str) -> Optional[str]:
        url = "https://prod-backend-auth-oapiyfa2ga-el.a.run.app/profile"
        try:
            async with self.session.get(
                url, headers=self.headers(telegram_query)
            ) as response:
                if response.status == 200:
                    profile_data = await response.json()
                    account_id = profile_data.get("id")
                    return account_id
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

    async def close(self):
        await self.session.close()
