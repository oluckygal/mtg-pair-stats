import mps_data as mps
import pandas as pd
import pytest

def test_as_dataframe_produces_equivalent_dataframe():
    test_data = {"expansion": ["EOE"], "event_type": ["sealed"], "won": [True]}
    test_dataframe = pd.DataFrame(data=test_data)
    game_data = mps.GameData(test_dataframe)
    game_data_dataframe = game_data.as_dataframe()
    assert(test_dataframe.equals(game_data_dataframe))
    game_data_dataframe.loc[0, 0] = "ECL"
    assert(not test_dataframe.equals(game_data_dataframe))

def test_get_card_names():
    game_data = mps.load_data.from_file("./tests/test_data/test_game_data.csv")
    #test caching
    for i in range(2):
        card_names = game_data.get_card_names()
        assert(card_names.count("Reach Through Mists") == 1)
        assert(card_names.count("Inspiration") == 1)
        assert(card_names.count("Jace's Ingenuity") == 1)
        assert(card_names.count("Opportunity") == 1)
        assert(card_names.count("Totally Lost") == 0)
    test_data = {"expansion": ["EOE"], "event_type": ["sealed"], "won": [True]}
    test_dataframe = pd.DataFrame(data=test_data)
    game_data = mps.GameData(test_dataframe)
    assert(len(game_data.get_card_names()) == 0)

def test_with_ever_in_hand():
    game_data = mps.load_data.from_file('./tests/test_data/test_game_data.csv')
    ever_in_hand_frame = game_data.with_ever_in_hand().as_dataframe()
    assert(ever_in_hand_frame["ever_in_hand_Reach Through Mists"][0] == True)
    assert(ever_in_hand_frame["ever_in_hand_Inspiration"][0] == True)
    assert(ever_in_hand_frame["ever_in_hand_Jace's Ingenuity"][0] == True)
    assert(ever_in_hand_frame["ever_in_hand_Opportunity"][0] == False)
    
    test_data = {"expansion": ["EOE"], "event_type": ["sealed"], "won": [True]}
    test_dataframe = pd.DataFrame(data=test_data)
    game_data = mps.GameData(test_dataframe)
    #shouldn't throw exception
    game_data.with_ever_in_hand()

def test_filter_by_in_deck():
    game_data = mps.load_data.from_file('./tests/test_data/test_game_data.csv')
    assert(game_data.filter_by_in_deck("Reach Through Mists").as_dataframe().shape[0] == 12)
    assert(game_data.filter_by_in_deck("Reach Through Mists", "Inspiration").as_dataframe().shape[0] == 11)
    assert(game_data.filter_by_in_deck("Reach Through Mists", "Jace's Ingenuity", "Inspiration").as_dataframe().shape[0] == 10)
    assert(game_data.filter_by_in_deck("Reach Through Mists", "Inspiration", "Jace's Ingenuity", "Opportunity").as_dataframe().shape[0] == 9)