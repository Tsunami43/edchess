from stockfish import Stockfish
from loguru import logger


class Chess:
    def __init__(self, stockfish_path: str):
        """
        Инициализация игры с подключением к шахматному движку Stockfish.

        :param stockfish_path: Путь к исполняемому файлу шахматного движка Stockfish
        """
        try:
            # Инициализируем движок Stockfish
            self.engine = Stockfish(stockfish_path)
            logger.info("Движок Stockfish успешно подключен.")
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

    def get_board_visual(self) -> None:
        """
        Возвращает визуализацию текущей позиции на доске.

        :return: Визуальное представление доски
        """
        try:
            board_visual = self.engine.get_board_visual()
            logger.info("Текущее состояние доски:\n" + board_visual)
        except Exception as e:
            logger.error(f"Ошибка при получении визуализации доски: {e}")
            raise Exception("Не удалось получить визуализацию доски.")
