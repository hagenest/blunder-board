from blunderboard.movegenerator import MoveGenerator
import RPi.GPIO as gpio


class BoardReader:
    hysteresis = 16
    default_gpio_mode = gpio.BCM
    default_row_gpios = [4, 5, 6, 12, 13, 16, 17, 19]
    default_column_gpios = [20, 21, 22, 23, 24, 25, 26, 27]

    def __init__(
        self,
        move_generator: MoveGenerator,
        row_gpios: list[int] = default_row_gpios,
        column_gpios: list[int] = default_column_gpios,
        gpio_mode=default_gpio_mode,
    ):
        gpio.setmode(gpio_mode)
        gpio.setup(column_gpios, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(row_gpios, gpio.OUT, initial=gpio.LOW)
        self.column_gpios = column_gpios
        self.row_gpios = row_gpios
        self.board_history: list[list[list[str]]] = []
        for _ in range(self.hysteresis):
            self.board_history.append(self._initial_board())
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
        next_board = self._empty_board()
        for i, row_gpio in enumerate(self.row_gpios):
            gpio.output(row_gpio, gpio.HIGH)
            for j, column_gpio in enumerate(self.column_gpios):
                if gpio.input(column_gpio):
                    next_board[i][j] = "x"
            gpio.output(row_gpio, gpio.LOW)
        self.board_history = [next_board] + self.board_history[:-1]

        # if the oldest half of the board history is not in inital position but all
        # newer boards are, reset game state
        for board in self.board_history[self.hysteresis // 2 :]:
            if self._is_initial_board(board):
                break
        else:
            for board in self.board_history[: self.hysteresis // 2]:
                if not self._is_initial_board(board):
                    break
            else:
                self.move_generator.reset()
                self.print()
                return

        for i in range(8):
            for j in range(8):
                # if the oldest half of the board history has a piece but no newer
                # boards have it, the piece was removed
                for board in self.board_history[self.hysteresis // 2 :]:
                    if board[i][j] == " ":
                        break
                else:
                    for board in self.board_history[: self.hysteresis // 2]:
                        if board[i][j] == "x":
                            break
                    else:
                        self.move_generator.take(i, j)
                        self.print()
        for i in range(8):
            for j in range(8):
                # if the oldest half of the board history doesn't have a piece but all
                # newer boards have it, the piece was placed
                for board in self.board_history[self.hysteresis // 2 :]:
                    if board[i][j] == "x":
                        break
                else:
                    for board in self.board_history[: self.hysteresis // 2]:
                        if board[i][j] == " ":
                            break
                    else:
                        self.move_generator.put(i, j)
                        self.print()

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
        self._print(self.board_history[0])
