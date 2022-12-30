from blunderboard.blunderevaluator import BlunderEvaluator
from blunderboard.boardreader import BoardReader
from blunderboard.movegenerator import MoveGenerator
import cProfile
from pstats import SortKey
from time import sleep


def main_content():
    try:
        blunder_evaluator = BlunderEvaluator()
        move_generator = MoveGenerator(blunder_evaluator)
        reader = BoardReader(move_generator)
        reader.scan()
        reader.print()
        while True:
            reader.scan()
            sleep(0.1)
    except KeyboardInterrupt:
        pass


def main():
    cProfile.runctx("main_content()", globals(), locals(), sort=SortKey.CUMULATIVE)
