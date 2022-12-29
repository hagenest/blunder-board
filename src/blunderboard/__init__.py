from blunderboard.boardreader import BoardReader


def main():
    reader = BoardReader()
    reader.scan()
    reader.print()
