import mps_data as mps
import pytest
def test_load_game_data():
    game_data = mps.load_data.from_file('./tests/test_data/game_data_public.EOE.PremierDraft.csv')
    assert(isinstance(game_data, mps.GameData))

def test_load_no_file():
    with pytest.raises(mps.errors.FileNotFoundError) as exception_info:
        mps.load_data.from_file('./tests/test_data/no-file.csv')
    assert(str(exception_info.value) == "No file found at \"./tests/test_data/no-file.csv\"")