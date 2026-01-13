import pandas as pd
from .errors import MandatoryColumnsMissingError
class GameData:
    _MANDATORY_COLUMNS_SET = set(["expansion","event_type","won"])
    _EVER_IN_HAND_PREFIX = "ever_in_hand_"
    def __init__(self, data: pd.DataFrame):
        self._validate_data(data)
        self._data = data.copy(deep=True)

    def _validate_data(self, data: pd.DataFrame) -> None:
        missing_columns = self._MANDATORY_COLUMNS_SET.difference(data.columns)
        if len(missing_columns) > 0:
            raise MandatoryColumnsMissingError(missing_columns)

    def _generate_card_names(self) -> list[str]:
        return self._data.filter(regex="^" + self._IN_DECK_PREFIX).columns.map(lambda label: label.split("_")[-1]).to_list()
    
    def get_card_names(self) -> list[str]:
        try:
            return self._card_names.copy()
        except AttributeError:
            self._card_names = self._generate_card_names()
            return self._card_names.copy()
    def as_dataframe(self) -> pd.DataFrame:
        return self._data.copy(deep=True)
    
    # def filter_games_by_card(self) -> GameData:
