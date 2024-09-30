from stockfish import Stockfish
from loguru import logger


class Chess:
    def __init__(self, iam: str, stockfish_path: str = "/usr/bin/stockfish"):
        """
        Инициализация игры с подключением к шахматному движку Stockfish.

        :param iam: Ваш цвет ('w' для белых, 'b' для черных)
        :param stockfish_path: Путь к исполняемому файлу шахматного движка Stockfish
        """
        if iam not in ["w", "b"]:
            raise ValueError("iam должен быть 'w' или 'b'.")

        self.iam = iam  # Сохраняем цвет игрока
        try:
            # Инициализируем движок Stockfish
            self.engine = Stockfish(stockfish_path)
            logger.info("Движок Stockfish успешно подключен.")
            self.current_fen = (
                None  # Инициализируем переменную для хранения текущей FEN
            )
        except Exception as e:
            logger.error(f"Ошибка при подключении к Stockfish: {e}")
            raise Exception("Ошибка подключения к Stockfish.")

    def set_fen_position(self, fen: str) -> None:
        """
        Устанавливает позицию на доске на основе FEN строки.

        :param fen: Строка позиции в формате FEN
        """
        try:
            self.engine.set_fen_position(fen)
            self.current_fen = fen  # Сохраняем текущую FEN
            logger.info(f"Позиция установлена по FEN: {fen}")
        except Exception as e:
            logger.error(f"Ошибка при установке FEN позиции: {e}")
            raise Exception("Ошибка при установке позиции по FEN.")

    def get_best_move(self) -> str:
        """
        Получает лучший ход с использованием шахматного движка.

        :return: Лучший ход в формате UCI (например, 'e2e4')
        """
        try:
            best_move = self.engine.get_best_move()
            logger.info(f"Лучший ход: {best_move}")
            return best_move
        except Exception as e:
            logger.error(f"Ошибка при получении лучшего хода: {e}")
            raise Exception("Не удалось получить лучший ход.")

    def get_turn(self) -> str:
        """
        Определяет, чья очередь ходить на основе текущей FEN.

        :return: 'w' если ходят белые, 'b' если черные
        """
        if self.current_fen is None:
            raise Exception(
                "Не установлена позиция. Пожалуйста, установите позицию с помощью set_fen_position."
            )

        # Последний символ FEN строки определяет чей ход
        turn = self.current_fen.split(" ")[1]
        logger.info(f"Текущий ход: {turn}")
        return turn

    def my_turn(self) -> bool:
        """
        Проверяет, является ли текущий ход вашим ходом.

        :return: True если ваш ход, иначе False
        """
        current_turn = self.get_turn()
        is_my_turn = current_turn == self.iam
        logger.info(f"Это мой ход: {is_my_turn}")
        return is_my_turn
