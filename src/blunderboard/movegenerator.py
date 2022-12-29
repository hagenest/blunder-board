from blunderboard.blunderevaluator import BlunderEvaluator


def coords_to_field(row: int, column: int):
    columns = "abcdefgh"
    return "%c%d" % (columns[column], row + 1)


class MoveGenerator:
    def __init__(self, blunder_evaluator: BlunderEvaluator):
        self.state: State = InitState(blunder_evaluator)

    def reset(self) -> None:
        print("reset")
        self.state = self.state.reset()

    def put(self, row: int, column: int) -> None:
        print("put %s" % coords_to_field(row, column))
        self.state = self.state.put(row, column)

    def take(self, row: int, column: int) -> None:
        print("take %s" % coords_to_field(row, column))
        self.state = self.state.take(row, column)


class State:
    def __init__(self, blunder_evaluator: BlunderEvaluator):
        self.blunder_evaluator = blunder_evaluator

    def reset(self) -> "State":
        self.blunder_evaluator.reset()
        return InitState(self.blunder_evaluator)

    def put(self, row: int, column: int) -> "State":
        print("ignored invalid put")
        return self

    def take(self, row: int, column: int) -> "State":
        print("ignored invalid take")
        return self


class InitState(State):
    def reset(self) -> State:
        super().reset()
        return self

    def take(self, row: int, column: int) -> State:
        return TakeState(self.blunder_evaluator, coords_to_field(row, column))


class TakeState(State):
    def __init__(self, blunder_evaluator: BlunderEvaluator, from_field: str):
        super().__init__(blunder_evaluator)
        self.from_field = from_field

    def put(self, row: int, column: int) -> State:
        to_field = coords_to_field(row, column)
        if self.from_field == to_field:
            print("ignored self-move")
            return InitState(self.blunder_evaluator)
        move = self.from_field + to_field
        print("move %s" % move)
        self.blunder_evaluator.move(move)
        return InitState(self.blunder_evaluator)

    def take(self, row: int, column: int) -> State:
        return TakeTakeState(
            self.blunder_evaluator, self.from_field, coords_to_field(row, column)
        )


class TakeTakeState(State):
    def __init__(
        self, blunder_evaluator: BlunderEvaluator, from_field: str, to_field: str
    ):
        super().__init__(blunder_evaluator)
        self.from_field = from_field
        self.to_field = to_field

    def put(self, row: int, column: int) -> State:
        field = coords_to_field(row, column)
        if self.to_field == field:
            move = self.from_field + field
        elif self.from_field == field:
            move = self.to_field + field
        else:
            print("ignored invalid put")
            return self
        print("move %s" % move)
        self.blunder_evaluator.move(move)
        return InitState(self.blunder_evaluator)
