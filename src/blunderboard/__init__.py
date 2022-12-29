from blunderboard.boardreader import BoardReader
from blunderboard.movegenerator import MoveGenerator
from time import sleep


def main():
    reader = BoardReader(MoveGenerator())
    while True:
        reader.scan()
        sleep(0.1)
