from enum import Enum


class ErrorType(str, Enum):
    """
    List of errors that can be handled individually by the user.
    """
    INVALID_API_KEY = "Unauthorized - Invalid API Key"
    SERVER_ERROR = "internal error"
    SERVER_OFFLINE = "server offline"
    REQUEST_ERROR = "error with the HTTP request"
    INVALID_RESULT = "json error"
    NO_FREE_PHONES = "no free phones"
    INCORRECT_COUNTRY = "country is incorrect"
    INCORRECT_PRODUCT = "product is incorrect"
    ORDER_NOT_FOUND = "order not found"
    ORDER_EXPIRED = "order not found"
    ORDER_HAS_SMS = "order has sms"
    ORDER_NO_SMS = "order no sms"
    HOSTING_ORDER = "hosting order"
    CANCEL_NEEDS_TIME = "you need to wait time"
    RECORD_NOT_FOUND = "record not found"
    API_KEY_LIMIT = "api limit is 100 requests per second"
    LIMIT_ERROR = "ip address limit is 100 requests per second"
    BALANCE_TOO_LOW = "not enough user balance"
    RATING_TOO_LOW = "not enough rating"
    BAD_COUNTRY = "bad country"
    BAD_OPERATOR = "bad operator"
    MISSING_COUNTRY = "select country"
    MISSING_OPERATOR = "select operator"
    MISSING_PRODUCT = "no product"
    OTHER = ""

    @classmethod
    def contains(cls, value) -> bool:
        try:
            cls(value)
        except:
            return False
        return True


class FiveSimError(Exception):
    """
    An error returned by the 5 SIM API.
    """

    def __init__(self, type: ErrorType, description: str = None) -> None:
        self.__type = type
        super().__init__(description if description is not None else self.__type.value)

    def get_description(self) -> str:
        return super.message if hasattr(super, "message") else ""

    def get_error(self) -> ErrorType:
        return self.__type
