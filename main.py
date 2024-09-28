import asyncio
from app.run import start_execute


async def main():
    await start_execute()


if __name__ == "__main__":
    asyncio.run(main())
