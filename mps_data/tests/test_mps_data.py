import mps_data as mps
import pytest
def test_load_game_data():
    game_data = mps.load_data.from_file('./tests/test_data/test_game_data.csv')
    assert(isinstance(game_data, mps.GameData))

def test_load_no_file():
    error_message = 'No file found at "./tests/test_data/no-file.csv"'
    with pytest.raises(mps.errors.FileNotFoundError) as exception_info:
        mps.load_data.from_file('./tests/test_data/no-file.csv')
    assert(str(exception_info.value) == error_message)

def test_load_irrelevant_file():
    error_message = 'File at "./tests/test_data/jabberwocky.txt" doesn\'t appear to contain 17lands game data'
    with pytest.raises(mps.errors.NonCsvDataError) as exception_info:
        mps.load_data.from_file('./tests/test_data/jabberwocky.txt')
    assert(str(exception_info.value) == error_message)