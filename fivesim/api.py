from typing import Any
from fivesim.errors import BadRequestError
from fivesim.order import ActivationProduct, Country, HostingProduct, Language, Operator
from fivesim.request import _APIRequest
from fivesim.response import CountryInformation, ProductInformation, _parse_guest_countries, _parse_guest_prices, _parse_guest_products


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)


class GuestAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/guest/", auth_token=api_key)

    def get_products(self, country: Country, operator: Operator) -> dict[ActivationProduct | HostingProduct, ProductInformation]:
        """
        Get available products by country.

        :param country: Country selection, ANY_COUNTRY is possible
        :param operator: Operator selection, ANY_OPERATOR is possible
        :return: dictionary with the association between a Product and its information
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=False,
            path=f"products/{country}/{operator}"
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_guest_products
        )

    def get_prices(self, country: Country = None, product: ActivationProduct = None) -> dict[Country, dict[ActivationProduct, dict[Operator, ProductInformation]]]:
        """
        Get prices.
        If country and product aren't provided, all the options will be returned.
        If country is provided, only the prices of the products for this country will be returned.
        If product is provided, there is a filter on the product.
        If country and product are provided, a specific filter will be used.

        :param country: Country selection
        :param product: Product selection
        :return: A dictionary that you can iterate over in a cycle or get a specific ProductInformation using [Country][Product][Operator]
        :raises FiveSimError: if the response is invalid
        """
        params: dict[str, str] = dict()
        if country != Country.ANY_COUNTRY and country is None:
            params["country"] = country
        if product is not None:
            params["product"] = product
        api_result = super()._GET(
            use_token=False,
            path="prices",
            parameters=params
        )
        if api_result.body == "null":
            raise BadRequestError("Product isn't available for the selected country")
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_guest_prices
        )

    def get_notification(self, lang: Language) -> str:
        """
        Get 5SIM notification.

        :param lang: Language of notification, Russian or English
        :return: notification text
        """
        if lang != lang.ENGLISH and lang != lang.RUSSIAN:
            raise ValueError("Language must be english or russian")
        try:
            api_result = super()._GET(
                use_token=True,
                path=f"flash/{lang}"
            )
            return super()._parse_json(input=api_result.body, need_keys=["text"])["text"]
        except:
            return ""

    def get_countries(self) -> dict[Country, CountryInformation]:
        """
        Get a list of all countries and their information.

        :return: dict of countries associated with their prefix and other data
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=False,
            path="countries"
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_guest_countries
        )


class VendorAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/vendor/", auth_token=api_key)
