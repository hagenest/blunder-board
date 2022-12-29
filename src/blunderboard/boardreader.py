from blunderboard.movegenerator import MoveGenerator
import RPi.GPIO as gpio


class BoardReader:
    default_gpio_mode = gpio.BCM
    default_row_gpios = [4, 5, 6, 12, 13, 16, 17, 19]
    default_column_gpios = [20, 21, 22, 23, 24, 25, 26, 27]

    def __init__(
        self,
        move_generator: MoveGenerator,
        rows: list[int] = default_row_gpios,
        columns: list[int] = default_column_gpios,
        gpio_mode=default_gpio_mode,
    ):
        gpio.setmode(gpio_mode)
        gpio.setup(columns, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(rows, gpio.OUT, initial=gpio.LOW)
        self.columns = columns
        self.rows = rows
        self.board = self._empty_board()
        self.move_generator = move_generator

    def __del__(self):
        gpio.cleanup()

    def _empty_board(self) -> list[list[str]]:
        board = []
        for i in range(8):
            board.append([" "] * 8)
        return board

    def _initial_board(self) -> list[list[str]]:
        board = []
        for i in range(2):
            board.append(["x"] * 8)
        for i in range(2, 6):
            board.append([" "] * 8)
        for i in range(6, 8):
            board.append(["x"] * 8)
        return board

    def _is_initial_board(self, board) -> bool:
        initial_board = self._initial_board()
        for i, row in enumerate(board):
            for j, field in enumerate(row):
                if field != initial_board[i][j]:
                    return False
        return True

    def scan(self) -> None:
        board = self._initial_board()
        for i, row_gpio in enumerate(self.rows):
            gpio.output(row_gpio, gpio.HIGH)
            for j, column_gpio in enumerate(self.columns):
                if gpio.input(column_gpio):
                    board[i][j] = "x"
                else:
                    board[i][j] = " "
            gpio.output(row_gpio, gpio.LOW)

        if not self._is_initial_board(self.board) and self._is_initial_board(board):
            self.move_generator.reset()
            self.board = board
            return

        for i, row in enumerate(board):
            for j, field in enumerate(row):
                if field == " " and self.board[i][j] == "x":
                    self.move_generator.take(i, j)
        for i, row in enumerate(board):
            for j, field in enumerate(row):
                if field == "x" and self.board[i][j] == " ":
                    self.move_generator.put(i, j)
        self.board = board

    def _print(self, board) -> None:
        print("  a b c d e f g h")
        print(" +---------------+")
        for i, row in reversed(list(enumerate(board))):
            print("%d|" % (i + 1), end="")
            for j, field in enumerate(row):
                print(field, end="")
                if j == 7:
                    print("|%d" % (i + 1))
                else:
                    print(" ", end="")
        print(" +---------------+")
        print("  a b c d e f g h")

    def print(self) -> None:
        self._print(self.board)
