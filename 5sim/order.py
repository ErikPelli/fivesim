from enum import Enum

class Status(str, Enum):
    PENDING = 'preparation'
    RECEIVED = 'waiting of receipt of SMS'
    CANCELED = 'is cancelled'
    TIMEOUT = 'a timeout'
    FINISHED = 'is complete'
    BANNED = 'number banned, when number already used'

    """
    Get the description of the current status.
    """
    def get_description(self) -> str:
        return self.value

    """
    Create a new instance of the Status enum.
    :param status: the uppercase key
    """
    @classmethod
    def from_status_string(cls, status: str) -> str:
        return cls[status]