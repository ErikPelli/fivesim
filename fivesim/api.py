from fivesim.errors import BadRequestError
from fivesim.order import ActivationProduct, Category, Country, HostingProduct, Language, Operator, VendorPaymentMethod, VendorPaymentSystem
from fivesim.request import _APIRequest
from fivesim.response import CountryInformation, ProductInformation, VendorWallet, _parse_guest_countries, _parse_guest_prices, _parse_guest_products


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)

    def balance_request(self):
        pass

    def order_history(self):
        pass

    def payments_history(self):
        pass


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
            raise BadRequestError("Product isn't available for the country")
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

    def statistic(self):
        pass

    def get_wallets_reserve(self) -> VendorWallet:
        """
        Get the wallet balance for the vendor.

        :return: list of balances (VendorWallet)
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path="wallets"
        )
        parsed = super()._parse_json(
            input=api_result.body,
            need_keys=[
                payment_system.value for payment_system in VendorPaymentSystem
            ]
        )
        result = VendorWallet()
        for payment_system in VendorPaymentSystem:
            payment_name = payment_system.value
            setattr(result, payment_name, parsed[payment_name])
        return result

    def orders_history(self, category: Category, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None):
        """
        Get the vendor orders history.

        :return: dict with the Array keys "Data", "ProductNames", "Statuses" and the Int key "Total"
        :raises FiveSimError: if the response is invalid
        """
        params: dict[str, str] = {"category": category.value}
        if results_per_page is not None:
            params["limit"] = str(results_per_page)
        if page_number is not None:
            params["offset"] = str(page_number)
        if order_by_field is not None:
            params["order"] = order_by_field
        if reverse_order is not None:
            params["reverse"] = "true" if reverse_order else "false"
        api_result = super()._GET(
            use_token=True,
            path="orders",
            parameters=params
        )
        return super()._parse_json(
            input=api_result.body,
            need_keys=["Data", "ProductNames", "Statuses", "Total"]
        )

    def payments_history(self, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None):
        """
        Get the vendor payments history.

        :return: dict with the Array keys "Data", "PaymentProviders", "PaymentStatuses", "PaymentTypes" and the Int key "Total"
        :raises FiveSimError: if the response is invalid
        """
        params: dict[str, str] = dict()
        if results_per_page is not None:
            params["limit"] = str(results_per_page)
        if page_number is not None:
            params["offset"] = str(page_number)
        if order_by_field is not None:
            params["order"] = order_by_field
        if reverse_order is not None:
            params["reverse"] = "true" if reverse_order else "false"
        api_result = super()._GET(
            use_token=True,
            path="orders",
            parameters=params
        )
        return super()._parse_json(
            input=api_result.body,
            need_keys=["Data", "PaymentProviders", "PaymentStatuses", "PaymentTypes", "Total"]
        )

    def create_payout(self, receiver: str, method: VendorPaymentMethod, amount: int, fee: VendorPaymentSystem) -> None:
        """
        Withdraw money from the 5SIM vendor account.

        :raises FiveSimError: if the response is invalid
        """
        super()._GET(
            use_token=True,
            path="withdraw",
            data={
                receiver: receiver,
                method: method.value,
                amount: str(amount),
                fee: fee.value
            }
        )
