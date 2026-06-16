from ... import GameData
import pandas as pd
class BothDrawnWinData:
    _CARD1_DRAWN_COLUMN_INDEX = "card1_drawn"
    _CARD2_DRAWN_COLUMN_INDEX = "card2_drawn"
    _CARD1_INDEX = "card1"
    _CARD2_INDEX = "card2"

    def __init__(self, data: GameData):
        cards = data.get_card_names()
        both_drawn_data_collector = []
        in_hand_data = data.with_ever_in_hand()
        for card1 in range(len(cards)):
            for card2 in range(card1 + 1, len(cards)):
                card_pair_data = self._generate_win_data_for_card_pair(cards[card1], cards[card2], in_hand_data)
                for card_pair_dataframe in card_pair_data:
                    both_drawn_data_collector.append(card_pair_dataframe)
            print(card1)
        self._data = pd.concat(both_drawn_data_collector, axis=0, ignore_index=True)

    def _move_card_names_to_data(self, data: pd.DataFrame, card1: str, card2: str) -> pd.DataFrame:
        card_stats = data.rename(
            columns={GameData.EVER_IN_HAND_PREFIX + card1 : self._CARD1_DRAWN_COLUMN_INDEX, 
                     GameData.EVER_IN_HAND_PREFIX + card2 : self._CARD2_DRAWN_COLUMN_INDEX})
        card_stats[self._CARD1_INDEX] = card1
        card_stats[self._CARD2_INDEX] = card2
        return card_stats
             

    def _generate_win_data_for_card_pair(self, card1: str, card2: str, data: GameData) -> list[pd.DataFrame]: 
        in_deck_data = data.with_ever_in_hand().filter_by_in_deck(card1, card2).as_dataframe()

        card1_in_hand_column = GameData.EVER_IN_HAND_PREFIX + card1
        card2_in_hand_column = GameData.EVER_IN_HAND_PREFIX + card2
        
        card_pair_filtered_data = in_deck_data.filter([
            GameData.WON_COLUMN_INDEX, 
            card1_in_hand_column, 
            card2_in_hand_column])
        card_pair_group_by = card_pair_filtered_data.groupby(by=[card1_in_hand_column, card2_in_hand_column])
        card_pair_stats = card_pair_group_by.aggregate(
            games=pd.NamedAgg(column=GameData.WON_COLUMN_INDEX, aggfunc="count"), 
            winrate=pd.NamedAgg(column=GameData.WON_COLUMN_INDEX, aggfunc="mean")).reset_index()
        card1_data = self._move_card_names_to_data(card_pair_stats, card1, card2)
        card2_data = self._move_card_names_to_data(card_pair_stats, card2, card1)
        return [card1_data, card2_data]
    
    def as_dataframe(self) -> pd.DataFrame:
        return self._data.copy(deep=True)
    
    def as_dict(self) -> dict:
        cards = self._data["card1"].unique()
        card_index_dict = {}
        for card1 in cards:
            card1_dict = {}
            for card2 in cards:
                if card1 == card2:
                    continue
                card_pair_data = self._data[(self._data["card1"] == card1) & (self._data["card2"] == card2)]
                card1_dict[card2] = {
                    "Both In Deck Games": card_pair_data["games"].sum(),
                    "Neither Drawn Winrate": card_pair_data[(card_pair_data["card1_drawn"] == False) & (card_pair_data["card2_drawn"] == False)]["winrate"].mean(),
                    "First Drawn Winrate": card_pair_data[(card_pair_data["card1_drawn"] == True) & (card_pair_data["card2_drawn"] == False)]["winrate"].mean(),
                    "Second Drawn Winrate": card_pair_data[(card_pair_data["card1_drawn"] == False) & (card_pair_data["card2_drawn"] == True)]["winrate"].mean(),
                    "Both Drawn Winrate": card_pair_data[(card_pair_data["card1_drawn"] == True) & (card_pair_data["card2_drawn"] == True)]["winrate"].mean(),
                }
            card_index_dict[card1] = card1_dict
        return card_index_dict
            

            

