class FiveSimError(Exception):
    '''An error returned by the 5 SIM API'''

class InvalidAPIKeyError(FiveSimError):
    '''Raised when the API Key is invalid'''
    def __init__(self) -> None:
        super().__init__("Invalid API Key")

class BadRequestError(FiveSimError):
    '''Raised when there is an error, with its description'''
    def __init__(self, description: str) -> None:
        super().__init__(description)