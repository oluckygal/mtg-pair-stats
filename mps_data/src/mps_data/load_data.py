from .game_data import GameData
from .errors import FileNotFoundError
from .errors import NonCsvDataError
import os.path
import pandas as pd


def _does_file_exist(filepath: str):
    return os.path.isfile(filepath)

def _load_csv_game_data(filepath):
    try:
        pd.read_csv(filepath)
    except pd.errors.ParserError:
        raise NonCsvDataError(filepath)
    
def from_file(filepath: str):
    if not _does_file_exist(filepath):
        raise FileNotFoundError(filepath)
    _load_csv_game_data(filepath)
    return GameData()

