import mps_data as mps
import pandas as pd
import pytest

def test_create_both_drawn_win_data():
    game_data = mps.load_data.from_file("./tests/test_data/test_both_drawn_win_data.csv")
    both_drawn_win_data = mps.data_processing.create_both_drawn_win_data(game_data)
    both_drawn_win_dataframe = both_drawn_win_data.as_dataframe()
    reach_insp_data = both_drawn_win_dataframe[(both_drawn_win_dataframe["card1"] == "Reach Through Mists") & (both_drawn_win_dataframe["card2"] == "Inspiration")]
    
    neither_drawn_data = reach_insp_data[~reach_insp_data["card1_drawn"] & ~reach_insp_data["card2_drawn"]]
    assert(len(neither_drawn_data.index) == 1)
    assert(neither_drawn_data["games"].iloc[0] == 2)
    assert(neither_drawn_data["winrate"].iloc[0] == 0.5)

    card1_drawn_data = reach_insp_data[reach_insp_data["card1_drawn"] & ~reach_insp_data["card2_drawn"]]
    assert(len(card1_drawn_data.index) == 1)
    assert(card1_drawn_data["games"].iloc[0] == 2)
    assert(card1_drawn_data["winrate"].iloc[0] == 0.5)

    card2_drawn_data = reach_insp_data[~reach_insp_data["card1_drawn"] & reach_insp_data["card2_drawn"]]
    assert(len(card2_drawn_data.index) == 1)
    assert(card2_drawn_data["games"].iloc[0] == 4)
    assert(card2_drawn_data["winrate"].iloc[0] == 0.25)

    both_drawn_data = reach_insp_data[reach_insp_data["card1_drawn"] & reach_insp_data["card2_drawn"]]
    assert(len(both_drawn_data.index == 1))
    assert(both_drawn_data["games"].iloc[0] == 2)
    assert(both_drawn_data["winrate"].iloc[0] == 0.5)

    insp_reach_data = both_drawn_win_dataframe[(both_drawn_win_dataframe["card1"] == "Inspiration") & (both_drawn_win_dataframe["card2"] == "Reach Through Mists")]

    #should be same data but with card1 and card2 swapped
    card1_drawn_data = insp_reach_data[insp_reach_data["card1_drawn"] & ~insp_reach_data["card2_drawn"]]
    assert(len(card1_drawn_data.index) == 1)
    assert(card1_drawn_data["games"].iloc[0] == 4)
    assert(card1_drawn_data["winrate"].iloc[0] == 0.25)

    card2_drawn_data = insp_reach_data[~insp_reach_data["card1_drawn"] & insp_reach_data["card2_drawn"]]
    assert(len(card2_drawn_data.index) == 1)
    assert(card2_drawn_data["games"].iloc[0] == 2)
    assert(card2_drawn_data["winrate"].iloc[0] == 0.5)

def test_as_dict():
    game_data = mps.load_data.from_file("./tests/test_data/test_both_drawn_win_data.csv")
    both_drawn_win_data = mps.data_processing.create_both_drawn_win_data(game_data)
    both_drawn_win_dict = both_drawn_win_data.as_dict()
    reach_insp_dict = both_drawn_win_dict["Reach Through Mists"]["Inspiration"]
    assert(reach_insp_dict["Both In Deck Games"] == 10)
    assert(reach_insp_dict["Neither Drawn Winrate"] == 0.5)
    assert(reach_insp_dict["First Drawn Winrate"] == 0.5)
    assert(reach_insp_dict["Second Drawn Winrate"] == 0.25)
    assert(reach_insp_dict["Both Drawn Winrate"] == 0.5)