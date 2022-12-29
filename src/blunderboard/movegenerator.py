class MoveGenerator:
    columns = "abcdefgh"

    def reset(self) -> None:
        print("reset")

    def put(self, row: int, column: int) -> None:
        print("put %c%d" % (self.columns[column], row + 1))

    def take(self, row: int, column: int) -> None:
        print("take %c%d" % (self.columns[column], row + 1))
