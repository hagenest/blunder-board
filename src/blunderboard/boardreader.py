import RPi.GPIO as gpio


class BoardReader:
    default_gpio_mode = gpio.BCM
    default_row_gpios = [4, 5, 6, 12, 13, 16, 17, 19]
    default_column_gpios = [20, 21, 22, 23, 24, 25, 26, 27]

    def __init__(
        self,
        rows=default_row_gpios,
        columns=default_column_gpios,
        gpio_mode=default_gpio_mode,
    ):
        gpio.setmode(gpio_mode)
        gpio.setup(columns, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(rows, gpio.OUT, initial=gpio.LOW)
        self.columns = columns
        self.rows = rows

    def __del__(self):
        gpio.cleanup()

    def scan(self) -> None:
        print("  a b c d e f g h")
        print(" +---------------+")
        for i, row in enumerate(self.rows):
            print("%d|" % (i + 1), end="")
            gpio.output(row, gpio.HIGH)
            for j, column in enumerate(self.columns):
                if gpio.input(column):
                    print("x", end="")
                else:
                    print(" ", end="")
                if j == 7:
                    print("|", end="")
                else:
                    print(" ", end="")
            gpio.output(row, gpio.LOW)
            print("")
