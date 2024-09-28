from stockfish import Stockfish
import logging

# Настройка логирования
logging.basicConfig(
    filename="chess_game.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class ChessGameWithStockfish:
    def __init__(self, stockfish_path: str):
        """
        Инициализация игры с подключением к шахматному движку Stockfish.

        :param stockfish_path: Путь к исполняемому файлу шахматного движка Stockfish
        """
        try:
            # Инициализируем движок Stockfish
            self.stockfish = Stockfish(stockfish_path)
            logging.info("Движок Stockfish успешно подключен.")
        except Exception as e:
            logging.error(f"Ошибка при подключении к Stockfish: {e}")
            raise Exception("Ошибка подключения к Stockfish.")

    def set_position(self, moves):
        """
        Устанавливает позицию по последовательности ходов.

        :param moves: Список ходов в формате UCI (например, ['e2e4', 'e7e5'])
        """
        try:
            self.stockfish.set_position(moves)
            logging.info(f"Позиция установлена по ходам: {moves}")
        except Exception as e:
            logging.error(f"Ошибка при установке позиции: {e}")
            raise Exception("Ошибка при установке позиции.")

    def get_best_move(self):
        """
        Возвращает лучший ход, рассчитанный движком Stockfish.

        :return: Лучшая шахматная запись хода (например, 'e2e4')
        """
        try:
            best_move = self.stockfish.get_best_move()
            logging.info(f"Лучший ход: {best_move}")
            return best_move
        except Exception as e:
            logging.error(f"Ошибка при получении лучшего хода: {e}")
            raise Exception("Не удалось получить лучший ход.")

    def make_move(self, move):
        """
        Выполняет ход, добавляя его к текущей позиции.

        :param move: Ход в формате UCI (например, 'e2e4')
        """
        try:
            self.stockfish.make_moves_from_current_position([move])
            logging.info(f"Ход {move} выполнен.")
        except Exception as e:
            logging.error(f"Ошибка при выполнении хода: {e}")
            raise Exception("Не удалось выполнить ход.")

    def get_board_visual(self):
        """
        Возвращает визуализацию текущей позиции на доске.

        :return: Визуальное представление доски
        """
        try:
            board_visual = self.stockfish.get_board_visual()
            print(board_visual)
            logging.info("Текущее состояние доски:\n" + board_visual)
        except Exception as e:
            logging.error(f"Ошибка при получении визуализации доски: {e}")
            raise Exception("Не удалось получить визуализацию доски.")

    def is_game_over(self):
        """
        Проверка на окончание игры.

        :return: True, если игра окончена (мат, пат и т.д.), иначе False
        """
        try:
            if (
                self.stockfish.get_best_move() == "0000"
            ):  # Если движок не может сделать ход, значит, игра окончена
                logging.info("Игра окончена.")
                return True
            return False
        except Exception as e:
            logging.error(f"Ошибка при проверке окончания игры: {e}")
            raise Exception("Не удалось проверить окончание игры.")

    def set_fen_position(self, fen: str):
        """
        Устанавливает позицию по строке FEN.

        :param fen: Строка позиции в формате FEN
        """
        try:
            self.stockfish.set_fen_position(fen)
            logging.info(f"Позиция установлена по FEN: {fen}")
        except Exception as e:
            logging.error(f"Ошибка при установке FEN позиции: {e}")
            raise Exception("Ошибка при установке позиции по FEN.")

    def set_skill_level(self, level: int):
        """
        Устанавливает уровень игры Stockfish (0-20).

        :param level: Уровень от 0 (слабый) до 20 (сильный)
        """
        try:
            self.stockfish.set_skill_level(level)
            logging.info(f"Уровень игры Stockfish установлен на {level}")
        except Exception as e:
            logging.error(f"Ошибка при установке уровня игры: {e}")
            raise Exception("Не удалось установить уровень игры Stockfish.")

    def close(self):
        """
        Завершает работу с движком Stockfish.
        """
        logging.info("Завершение работы с движком Stockfish.")
