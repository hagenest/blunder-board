import os
from pathlib import Path
from pygame import mixer
import random
from stockfish import Stockfish

sound_path = Path("../../sounds")


class BlunderEvaluator:
    default_engine_settings = {
        "Debug Log File": "stocklog.txt",
        "Contempt": 0,
        "Min Split Depth": 0,
        "Threads": 1,
        # More threads will make the engine stronger, but should be kept at less than
        # the number of logical processors on your computer.
        "Ponder": "false",
        "Hash": 256,
        # Default size is 16 MB. It's recommended that you increase this value, but keep
        # it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to
        # 2048 (11th power of 2).
        "MultiPV": 1,
        "Skill Level": 20,
        "Move Overhead": 10,
        "Minimum Thinking Time": 20,
        "Slow Mover": 100,
        "UCI_Chess960": "false",
        "UCI_LimitStrength": "false",
        "UCI_Elo": 1350,
        # "NNUE": "true", # TODO Find out if NNUE can be used with the python wrapper
    }

    def __init__(self, engine_settings: dict = default_engine_settings):
        self.engine = Stockfish("/usr/bin/stockfish")
        self.settings = engine_settings
        self.engine.update_engine_parameters(self.settings)
        self.current_evaluation = (
            self.engine.get_evaluation()
        )  # This is not necessary, now that I think about it.
        self.evaluations: list[dict] = []
        self.current_wdl = self.engine.get_wdl_stats()
        self.wdls: list[tuple[int, int, int]] = []
        self.engine.set_position()

    def reset(self):
        self.engine.set_position()

    def move(self, move) -> None:
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
                # If the played move was a blunder play a random sound from the blunder
                # path
                self.play_sound("blunder")
                print("Blunder!")
        else:
            print("Invalid move")
            self.play_sound("illegal")

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
        return False

    @staticmethod
    def play_sound(move_type: str) -> None:
        """
        Plays a random sound for the type of move (blunder, illegal)
        :param move_type: str
        :return: None
        """
        path = sound_path / move_type
        mixer.init()
        mixer.music.load("sounds/" + random.choice(os.listdir(path)))
        mixer.music.play()
        # while mixer.music.get_busy():
        #     time.sleep(0.)
        # I guess we won't want this, since it will block the main thread.

    def get_board(self) -> str:
        """
        Returns the current board state
        :return: str
        """
        return self.engine.get_board_visual()
