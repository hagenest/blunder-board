from stockfish import Stockfish
from playsound import playsound
from pathlib import Path
import random

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

    def __init__(self, settings: dict):
        self.engine = Stockfish("/usr/local/bin/stockfish")
        self.settings = settings
        self.engine.update_engine_parameters(self.settings)
        self.matrix = BoardReader()
        self.current_evaluation = self.engine.get_evaluation()
        self.evaluations = []
        self.engine.set_position()

        def make_move(move) -> None:
            """
            Makes a move on the board and updates the game state
            :param move:
            :return: None
            """
            if self.engine.is_move_correct(move):
                self.engine.make_moves_from_current_position([move])
                self.current_evaluation = self.engine.get_evaluation()
                self.evaluations.append(self.current_evaluation)
            if move_was_blunder():
                # If the played move was a blunder play a random sound from the sound path
                playsound(random.choice(sound_path))

        def move_was_blunder() -> bool:
            """
            Returns true if the last move was a blunder
            :return: bool
            """
            previous_evaluation = self.evaluations[-1]
            return self.current_evaluation["value"] < (previous_evaluation["value"] + 3)  # TODO This is not a
            # particularly good way to identify a blunder

    def __str__(self):
        return ""


