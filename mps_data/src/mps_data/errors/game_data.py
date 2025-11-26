_COLUMNS_MISSING_TEMPLATE = "Missing mandatory columns: {columns}"

class MandatoryColumnsMissingError(Exception):
    def __init__(self, columns: set[str]):
        self.columns = columns
        message = _COLUMNS_MISSING_TEMPLATE.format(columns=columns)
        super().__init__(message)