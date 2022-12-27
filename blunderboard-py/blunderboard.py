from stockfish import Stockfish
from pygame import mixer
import time
from pathlib import Path
import random
import os
#import RPi.GPIO as GPIO

settings = {
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 10,
    # More threads will make the engine stronger, but should be kept at less than the number of logical processors on
    # your computer.
    "Ponder": "false",
    "Hash": 8100,
    # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g.,
    # if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 1350,
    "NNUE": "true",
}

sound_path = Path("sounds")


class BoardReader:
    """
    A class containing methods to read the board state through the GPIO matrix.
    """

    def __init__(self):
        pass

    # TODO WIP

    def get_latest_move(self):
        return ""


def play_sound() -> None:
    """
    Plays a random sound from the sound path
    :return: None
    """
    mixer.init()
    mixer.music.load("sounds/" + random.choice(os.listdir(sound_path)))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)


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
        self.current_wdl = self.engine.get_wdl_stats()
        self.wdls = []
        self.engine.set_position()

    def move_was_blunder(self) -> bool:
        """
        Returns true if the last move was a blunder
        :return: bool
        """
        if len(self.wdls) > 1:  # Don't check for blunders on the first move
            previous_wdl = self.wdls[len(self.evaluations) - 2]
            if abs(previous_wdl[0] - self.current_wdl[0]) > 300:
                return True
            elif abs(previous_wdl[2] - self.current_wdl[2]) > 300:
                return True
            else:
                return False

    def make_move(self, move) -> None:
        """
        Makes a move on the board and updates the game state
        :param move: str
        :return: None
        """
        if self.engine.is_move_correct(move):
            self.engine.make_moves_from_current_position([move])
            self.current_evaluation = self.engine.get_evaluation()
            self.evaluations.append(self.current_evaluation)
            self.current_wdl = self.engine.get_wdl_stats()
            self.wdls.append(self.current_wdl)
            print(self.current_wdl)
            print(self.current_evaluation)
            if self.move_was_blunder():
                # If the played move was a blunder play a random sound from the sound path
                #play_sound()
                print("Blunder!")
        else:
            print("Invalid move")

    def __str__(self):
        return ""


test_game = Game(settings)

moves_manual = ["e2e4", "e7e6", "e4e5", "d7d5", "e5d6", "c7d6", "b1c3", "b8c6", "f1b5", "a7a6", "b5a4", "b7b5", "a4b3",
                "d6d5", "a2a4", "c8b7", "a4b5", "a6b5", "a1a8", "d8a8", "c3b5", "a8a5", "c2c4", "b7a6", "b5c3", "a6c4",
                "b3c4", "d5c4", "d1g4", "a5a1"]
for move in moves_manual:
    print(move)
    test_game.make_move(move)
