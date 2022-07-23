from request import _APIRequest


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)


class GuestAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/guest/", auth_token=api_key)


class VendorAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/vendor/", auth_token=api_key)
