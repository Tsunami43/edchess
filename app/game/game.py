from typing import Optional
from .chess import Chess
from .timer import Timer
from loguru import logger


class Oponent:
    def __init__(self, nickname: Optional[str], rating: Optional[int], color: str):
        self.nickname = nickname
        self.rating = rating
        self.color = color

    def __repr__(self):
        return f"Oponent(nickname={self.nickname}, rating={self.rating}, color={self.color})"


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
        self.oponent = Oponent(
            oponent_nickname, oponent_rating, "b" if color == "w" else "w"
        )
        self.id = id
        self.fen = fen
        self.chess = Chess()
        self.timer = Timer(
            time_remaining=timers.get(color),
            first_move_time_remaining=timers.get("first_move_time_left"),
            first=color == "w",
        )

    def ignore_oponent(self, color: bool = True) -> bool:
        ignores = ["Daddy"]
        if color:
            return self.oponent.nickname in ignores and self.color == "b"
        else:
            return self.oponent.nickname in ignores

    def get_turn(
        self,
    ) -> str:
        # Последний символ FEN строки определяет чей ход
        turn = self.fen.split(" ")[1]
        logger.info(f"Текущий ход: {turn}")
        return turn

    def get_move(self, depth: int = 10, time_limit: float = 1.5) -> str:
        self.chess.set_fen_position(self.fen)
        return self.chess.get_best_move(time_limit, depth)

    def get_moves(self, depth: int = 10, number: int = 3):
        self.chess.set_fen_position(self.fen)
        return self.chess.get_top_moves(depth=depth, number=number)
