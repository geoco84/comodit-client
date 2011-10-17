class PythonApiException(Exception):
    def __init__(self, message):
        self.message = message

class NotFoundException(PythonApiException):
    def __init__(self, message):
        self.message = message