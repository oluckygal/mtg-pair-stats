import mps_data as mps
import pandas as pd
import pytest

def test_to_dataframe_produces_equivalent_dataframe():
    test_data = {"expansion": ["EOE"], "event_type": ["sealed"], "won": [True]}
    test_dataframe = pd.DataFrame(data=test_data)
    game_data = mps.GameData(test_dataframe)
    game_data_dataframe = game_data.to_dataframe()
    assert(test_dataframe.equals(game_data_dataframe))
    game_data_dataframe.loc[0, 0] = "ECL"
    assert(not test_dataframe.equals(game_data_dataframe))
    
# def test_get_improvement_when_drawn_game_count():
#     game_data = mps.load_data.from_file('./tests/test_data/test_game_data.csv')
#     iwd_data = mps.data_processing.get_improvement_when_drawn(game_data)
#     assert(iwd_data.get_game_count("Reach Through Mists") == 8)