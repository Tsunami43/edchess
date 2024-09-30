import asyncio
import time
import asyncio


class PingClient:
    def __init__(self):
        self.prev_time = 0
        self.__prev_ping = 0
        self.__task = None

    async def start(self, client):
        async def task():
            while client.__stream:
                await client.send_message(
                    {
                        "rpc": {
                            "method": "ping",
                            "data": {"variation": {"prev_ping": self.prev_ping}},
                        },
                    }
                )
                self.prev_time = time.time()
                await asyncio.sleep(1)

        self.__task = asyncio.create_task(task())

    def stop(self):
        if self.__task:
            self.__task.cancel()

    @property
    def prev_ping(self) -> int:
        return self.__prev_ping

    @prev_ping.setter
    def prev_ping(self):
        self.__prev_ping = int(time.time() - self.prev_time)
