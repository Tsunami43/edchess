import time


class Timer:
    def __init__(
        self, time_remaining: int, first_move_time_remaining: int, first: bool
    ):
        self.time_remaining = time_remaining
        self.first = first
        self.first_move_time_remaining = first_move_time_remaining
        self.time = None

    def start(self):
        """Запускает таймер первого хода."""
        self.time = time.time()

    def stop(self) -> int:
        duration = int((time.time() - self.time) * 1000)
        if self.first:
            self.first = False
            return self.time_remaining + self.first_move_time_remaining - duration
        self.time_remaining = (
            self.time_remaining + self.first_move_time_remaining - duration
        )
        return self.time_remaining

    def get_turn(
        self,
    ) -> str:
        # Последний символ FEN строки определяет чей ход
        turn = fen.split(" ")[1]
        logger.info(f"Текущий ход: {turn}")
        return turn
