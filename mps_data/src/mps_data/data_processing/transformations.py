from .both_drawn_win_data import BothDrawnWinData
from ..game_data import GameData

def create_both_drawn_win_data(game_data: GameData) -> BothDrawnWinData:
    return BothDrawnWinData(game_data)