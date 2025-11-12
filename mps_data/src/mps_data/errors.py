class FileNotFoundError(Exception):
    _MESSAGE_TEMPLATE = "No file found at \"{path}\""
    def __init__(self, path):
        self.msg = self._MESSAGE_TEMPLATE.format(path=path)
        super().__init__(path)
    def __str__(self):
        return self.msg