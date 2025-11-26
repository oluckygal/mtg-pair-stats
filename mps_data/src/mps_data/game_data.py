import pandas as pd
from .errors import MandatoryColumnsMissingError
class GameData:
    _MANDATORY_COLUMNS_SET = set(["expansion","event_type","won"])
    def __init__(self, data: pd.DataFrame):
        self._validate_data(data)

    def _validate_data(self, data: pd.DataFrame):
        missing_columns = self._MANDATORY_COLUMNS_SET.difference(data.columns)
        if len(missing_columns) > 0:
            raise MandatoryColumnsMissingError(missing_columns)
