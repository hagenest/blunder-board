from stockfish import Stockfish
from playsound import playsound
from pathlib import Path
import random
from pgn_parser import parser, pgn

# import RPi.GPIO as GPIO

settings = {
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1,
    # More threads will make the engine stronger, but should be kept at less than the number of logical processors on
    # your computer.
    "Ponder": "false",
    "Hash": 16,
    # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g.,
    # if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 1350
}

sound_path = [Path("sounds/")]


class BoardReader:
    """
    A class containing methods to read the board state through the GPIO matrix.
    """

    def __init__(self):
        pass

    # TODO WIP

    def get_latest_move(self):
        return ""


class Game:
    """
    A class representing the game state
    """

    def __init__(self, engine_settings: dict):
        self.engine = Stockfish("/usr/bin/stockfish")
        self.settings = engine_settings
        self.engine.update_engine_parameters(self.settings)
        self.matrix = BoardReader()
        self.current_evaluation = self.engine.get_evaluation()  # This is not necessary, now that I think about it.
        self.evaluations = []
        self.engine.set_position()

    def move_was_blunder(self) -> bool:
        """
        Returns true if the last move was a blunder
        :return: bool
        """
        if len(self.evaluations) > 1:
            previous_evaluation = self.evaluations[-1]
            return abs(self.current_evaluation["value"] - previous_evaluation["value"]) > 300
            # TODO This is not a particularly good way to identify a blunder
        else:
            return False

    def make_move(self, move) -> None:
        """
        Makes a move on the board and updates the game state
        :param move:
        :return: None
        """
        if self.engine.is_move_correct(move):
            self.engine.make_moves_from_current_position([move])
            self.current_evaluation = self.engine.get_evaluation()
            self.evaluations.append(self.current_evaluation)
        if self.move_was_blunder():
            # If the played move was a blunder play a random sound from the sound path
            # playsound(random.choice(sound_path))
            print("Blunder!")

    def __str__(self):
        return ""


def get_moves_from_pgn(pgn_file: Path):
    """
    Returns a list of moves from a PGN file
    :param pgn_file: str
    :return: list
    """
    with open(pgn_file, "r") as f:
        pgn_file = f.read()
    return parser.parse(pgn_file, actions=pgn.Actions())


test_game = Game(settings)

pgn_path = Path("../spongeboyahoy_vs_tomlx.pgn")
moves = get_moves_from_pgn(pgn_path)
for i in range(1, 250):
    print(str(moves.move(i)).split(". ")[1].split(" ")[0])
    test_game.make_move(str(moves.move(i)).split(". ")[1].split(" ")[0])
    print(test_game.current_evaluation)
    test_game.make_move(str(moves.move(i)).split(". ")[1].split(" ")[1])
    print(test_game.current_evaluation)


