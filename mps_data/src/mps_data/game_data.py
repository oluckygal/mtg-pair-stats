import pandas as pd
from .errors import MandatoryColumnsMissingError
class GameData:
    WON_COLUMN_INDEX = "won"
    EXPANSION_COLUMN_INDEX = "expansion"
    EVENT_COLUMN_INDEX = "event_type"

    _MANDATORY_COLUMNS_SET = set([WON_COLUMN_INDEX, EXPANSION_COLUMN_INDEX, EVENT_COLUMN_INDEX])
    
    IN_DECK_PREFIX = "deck_"
    EVER_IN_HAND_PREFIX = "ever_in_hand_"
    IN_SIDEBOARD_PREFIX = "sideboard_"

    OPENING_HAND_PREFIX = "opening_hand_"
    DRAWN_PREFIX = "drawn_"
    TUTORED_PREFIX = "tutored_"

    _BASE_CARD_IN_HAND_PREFIXES = set([OPENING_HAND_PREFIX, DRAWN_PREFIX, TUTORED_PREFIX])
    _BASE_CARD_DATA_PREFIXES = _BASE_CARD_IN_HAND_PREFIXES.union(set([IN_DECK_PREFIX, IN_SIDEBOARD_PREFIX]))
    _ALL_CARD_DATA_PREFIXES = _BASE_CARD_DATA_PREFIXES.union(set([EVER_IN_HAND_PREFIX]))

    def __init__(self, data: pd.DataFrame):
        self._validate_data(data)
        self._data = data.copy(deep=True)

    def _validate_data(self, data: pd.DataFrame) -> None:
        missing_columns = self._MANDATORY_COLUMNS_SET.difference(data.columns)
        if len(missing_columns) > 0:
            raise MandatoryColumnsMissingError(missing_columns)

    def _generate_card_names(self) -> list[str]:
        return self._data.filter(regex="^" + self.IN_DECK_PREFIX).columns.map(lambda label: label.split("_")[-1]).to_list()
    
    def get_card_names(self) -> list[str]:
        try:
            return self._card_names.copy()
        except AttributeError:
            self._card_names = self._generate_card_names()
            return self._card_names.copy()
        

    def _add_ever_in_hand(self) -> "GameData":
        data = self._data.copy()
        for card_name in self.get_card_names():
            new_in_hand_column_label = self.EVER_IN_HAND_PREFIX + card_name
            data[new_in_hand_column_label] = False
            for base_in_hand_prefix in self._BASE_CARD_IN_HAND_PREFIXES:
                base_in_hand_column = data[base_in_hand_prefix + card_name]
                data[new_in_hand_column_label] = data[new_in_hand_column_label] | (base_in_hand_column > 0)
        return GameData(data)
        
        
    def with_ever_in_hand(self) -> "GameData":
        if len(self._data.filter(regex="^" + self.EVER_IN_HAND_PREFIX).columns) > 0:
            return self
        return self._add_ever_in_hand()
        
    def as_dataframe(self) -> pd.DataFrame:
        return self._data.copy(deep=True)
    
    def filter_by_in_deck(self, *cards: str) -> "GameData":
        filtered_data = self._data
        for card in cards:
            filtered_data = filtered_data[filtered_data[self.IN_DECK_PREFIX + card] > 0]
        return GameData(filtered_data)
    
    def get_format(self):
        return self._data["event_type"].loc[0]
    
    def get_set(self):
        return self._data["expansion"].loc[0]
