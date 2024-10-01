from typing import Optional
from .chess import Chess
from .timer import Timer


class Oponent:
    def __init__(self, nickname: Optional[str], rating: Optiona[int]):
        self.nickname = nickname
        self.rating = rating


class Game:
    def __init__(
        self,
        id: str,
        channel: str,
        fen: str,
        color: str,
        oponent_nickname: Optional[str],
        oponent_rating: Optional[int],
        timers: dict,
    ):
        self.channel = channel
        self.color = color
        self.oponent = Oponent(oponent_nickname, oponent_rating)
        self.id = id
        self.fen = fen
        self.chess = Chess()
        self.timer = Timer(
            time_remaining=timers.get(color),
            first_move_time_remaining=timers.get("first_move_time_left"),
            first=color == "w",
        )

    def get_turn(
        self,
    ) -> str:
        # Последний символ FEN строки определяет чей ход
        turn = self.fen.split(" ")[1]
        logger.info(f"Текущий ход: {turn}")
        return turn

    def get_move(self) -> str:
        return self.chess.get_best_move(self.fen)
