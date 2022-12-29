from blunderboard.blunderevaluator import BlunderEvaluator


class MoveGenerator:
    columns = "abcdefgh"

    def __init__(self, blunder_evaluator: BlunderEvaluator):
        self.blunder_evaluator = blunder_evaluator

    def reset(self) -> None:
        print("reset")
        self.blunder_evaluator.reset()

    def put(self, row: int, column: int) -> None:
        print("put %c%d" % (self.columns[column], row + 1))

    def take(self, row: int, column: int) -> None:
        print("take %c%d" % (self.columns[column], row + 1))
