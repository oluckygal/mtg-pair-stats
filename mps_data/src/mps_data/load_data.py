from .game_data import GameData
from .errors import FileNotFoundError
import os.path

def _does_file_exist(filepath: str):
    return os.path.isfile(filepath)

def from_file(filepath: str):
    if not _does_file_exist(filepath):
        raise FileNotFoundError(filepath)
    return GameData()

