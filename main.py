import asyncio
import os
from app.run import start_execute
from app.telegram.session import Session
from app.utils import Profile
from typing import List
from loguru import logger

SESSIONS_DIR = "sessions"

edchess_print = """
███████╗██████╗░░█████╗░██╗░░██╗███████╗░██████╗░██████╗
██╔════╝██╔══██╗██╔══██╗██║░░██║██╔════╝██╔════╝██╔════╝
█████╗░░██║░░██║██║░░╚═╝███████║█████╗░░╚█████╗░╚█████╗░
██╔══╝░░██║░░██║██║░░██╗██╔══██║██╔══╝░░░╚═══██╗░╚═══██╗
███████╗██████╔╝╚█████╔╝██║░░██║███████╗██████╔╝██████╔╝
╚══════╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░

1.Add new session
2.Run bot
"""


def get_sessions() -> List[str]:
    try:
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)
            logger.info(f"Directory '{SESSIONS_DIR}' created.")

        session_files = []

        for f in os.listdir(SESSIONS_DIR):

            if f.endswith(".session"):
                session_files.append(f.replace(".session", ""))

        logger.debug(f"Found: {len(session_files)} .session files")
        return session_files

    except Exception as e:
        logger.error(f"Error while processing files: {e}")
        return []


class NotFoundSession(Exception):
    pass


async def main():
    try:
        print(edchess_print)
        code = input("Input code menu: ")
        if int(code) not in [1, 2]:
            raise ValueError("Code invalid")
        name = input("Input session name: ")
        if code == "1":
            profile = Profile(name)
            session = Session(name, proxy_data=profile.proxy_data)
            await session.create()
        if code == "2":
            session_names = get_sessions()
            if name in session_names:
                await start_execute(name)
            else:
                raise NotFoundSession("Session `{name}` is not found")
    except Exception as e:
        logger.info(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
