from fivesim.api import UserAPI, GuestAPI, VendorAPI


class FiveSim:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.user = UserAPI(api_key=self.__api_key)
        self.guest = GuestAPI(api_key=self.__api_key)
        self.vendor = VendorAPI(api_key=self.__api_key)

    def __str__(self) -> str:
        return self.__api_key
