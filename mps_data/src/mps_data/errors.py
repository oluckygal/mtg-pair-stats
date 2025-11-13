class PathError(Exception):
    _MESSAGE_TEMPLATE='{path}'
    def __init__(self, path):
        message = self._MESSAGE_TEMPLATE.format(path=path)
        super().__init__(message)

class FileNotFoundError(PathError):
    _MESSAGE_TEMPLATE = 'No file found at "{path}"'

class NonCsvDataError(PathError):
    _MESSAGE_TEMPLATE = 'File at "{path}" doesn\'t appear to contain 17lands game data'