class Error(Exception):
    """Base class for other exceptions"""
    pass

class FileNotFoundError(Error):
    """Raised when a file has not been found"""
    pass

class JsonProcessingError(Error):
    """Raised when a JSON file could not be processed"""
    pass

class ArgumentsException(Error):
    """Raised when arguments could not be processed"""
    pass
