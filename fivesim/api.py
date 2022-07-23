from typing import Any
from fivesim.errors import FiveSimError
from fivesim.order import ActivationProduct, Country, HostingProduct, Language, Operator, Product
from fivesim.request import _APIRequest
from fivesim.response import ProductInformation, _parse_products


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)


class GuestAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/guest/", auth_token=api_key)

    def get_products(self, country: Country, operator: Operator) -> dict[Product, ProductInformation]:
        """
        Get available products by country.

        :param lang: Language of notification, Russian or English
        :return: notification text
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True, path=f"products/{country}/{operator}")
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_products
        )

    def get_notification(self, lang: Language) -> str:
        """
        Get notifications.

        :param lang: Language of notification, Russian or English
        :return: notification text
        :raises FiveSimError: if the response is invalid
        """
        if lang != lang.ENGLISH and lang != lang.RUSSIAN:
            raise ValueError("Language must be english or russian")
        result = super()._GET(use_token=True, path=f"flash/{lang}")
        try:
            return super()._parse_json(input=result.body, need_keys=["text"])["text"]
        except:
            return ""

    def get_countries(self):
        super()._GET(use_token=False, path="countries")


class VendorAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/vendor/", auth_token=api_key)
