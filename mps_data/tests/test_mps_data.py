import mps_data as mps
def test_load_game_data():
    game_data = mps.load_data.from_file('./game_data_public.EOE.PremierDraft.csv')
    assert(isinstance(game_data, mps.GameData))