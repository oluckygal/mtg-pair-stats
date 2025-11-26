FNF_MESSAGE_TEMPLATE = 'No file found at "{path}".'
NON_CSV_MESSAGE_TEMPLATE = 'File at "{path}" doesn\'t appear to contain 17lands game data.'
GDM_MESSAGE_TEMPLATE = 'File at "{path}" doesn\'t appear to contain 17lands game data. Missing columns: {columns}'

class PathError(Exception):
    _MESSAGE_TEMPLATE='{path}'
    def __init__(self, path: str):
        message = self._MESSAGE_TEMPLATE.format(path=path)
        super().__init__(message)

class FileNotFoundError(PathError):
    _MESSAGE_TEMPLATE = FNF_MESSAGE_TEMPLATE

class NonCsvDataError(PathError):
    _MESSAGE_TEMPLATE = NON_CSV_MESSAGE_TEMPLATE

class GameDataMissingError(Exception):
    _MESSAGE_TEMPLATE = GDM_MESSAGE_TEMPLATE
    def __init__(self, path: str, columns: set[str]):
        list_columns = list(columns)
        list_columns.sort()
        message = self._MESSAGE_TEMPLATE.format(path=path, columns=list_columns)
        super().__init__(message)
