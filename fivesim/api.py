from fivesim.errors import BadRequestError
from fivesim.order import(
    ActivationProduct,
    Category,
    Country,
    HostingProduct,
    Language,
    Operator,
    VendorPaymentMethod,
    VendorPaymentSystem
)
from fivesim.request import _APIRequest
from fivesim.response import(
    CountryInformation,
    OrdersHistory,
    PaymentsHistory,
    ProductInformation,
    ProfileInformation,
    VendorWallet,
    _parse_guest_countries,
    _parse_guest_prices,
    _parse_guest_products,
    _parse_orders_history,
    _parse_payments_history,
    _parse_profile_data
)


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)

    def get_user_data(self) -> ProfileInformation:
        """
        Get data about the user account.

        :return: Profile object with the data
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path="profile"
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_profile_data
        )

    def get_vendor_data(self) -> ProfileInformation:
        """
        Get data about the vendor account (available only for vendors).

        :return: Profile object with the data
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path="vendor"
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_profile_data
        )

    def get_orders_history(self, category: Category, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None) -> OrdersHistory:
        """
        Get the user orders history.

        :param category: Category of the orders requested
        :param results_per_page: Number of results to show on every page
        :param page_number: Number of the page to get, starting from 0 (first)
        :param order_by_field: Order the results by a specific field, default is "id"
        :param reverse_order: Show the results in reverse order (has to do with the previous one)
        :return: OrdersHistory object
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
            into_object=_parse_orders_history
        )

    def get_payments_history(self, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None) -> PaymentsHistory:
        """
        Get the user payments history.

        :param results_per_page: Number of results to show on every page
        :param page_number: Number of the page to get, starting from 0 (first)
        :param order_by_field: Order the results by a specific field, default is "id"
        :param reverse_order: Show the results in reverse order (has to do with the previous one)
        :return: PaymentsHistory object
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
            path="payments",
            parameters=params
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_payments_history
        )

    def reuse_number(self, product: ActivationProduct | HostingProduct, number: str) -> None:
        """
        Rebuy a 5SIM number, activation or hosting.

        :param product: Product to rebuy
        :param number: Telephone number to rebuy (with prefix, without + sign)
        :raises FiveSimError: if the response is invalid
        """
        super()._GET(
            use_token=True,
            path=f"reuse/{product.value}/{number}",
        )


class GuestAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/guest/", auth_token=api_key)

    def get_products(self, country: Country, operator: Operator) -> dict[ActivationProduct | HostingProduct, ProductInformation]:
        """
        Get available products by country.

        :param country: Country selection, ANY_COUNTRY is possible
        :param operator: Operator selection, ANY_OPERATOR is possible
        :return: Dict with the association between a Product and its information
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
        :return: Notification text
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

        :return: Dict of countries associated with their prefix and other data
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

    def get_wallets_reserve(self) -> VendorWallet:
        """
        Get the wallet balance for the vendor.

        :return: List of balances (VendorWallet)
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

    def get_orders_history(self, category: Category, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None) -> OrdersHistory:
        """
        Get the vendor orders history.

        :param category: Category of the orders requested
        :param results_per_page: Number of results to show on every page
        :param page_number: Number of the page to get, starting from 0 (first)
        :param order_by_field: Order the results by a specific field, default is "id"
        :param reverse_order: Show the results in reverse order (has to do with the previous one)
        :return: OrdersHistory object
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
            into_object=_parse_orders_history
        )

    def get_payments_history(self, results_per_page: int = None, page_number: int = None, order_by_field: str = None, reverse_order: bool = None) -> PaymentsHistory:
        """
        Get the vendor payments history.

        :param results_per_page: Number of results to show on every page
        :param page_number: Number of the page to get, starting from 0 (first)
        :param order_by_field: Order the results by a specific field, default is "id"
        :param reverse_order: Show the results in reverse order (has to do with the previous one)
        :return: PaymentsHistory object
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
            path="payments",
            parameters=params
        )
        return super()._parse_json(
            input=api_result.body,
            into_object=_parse_payments_history
        )

    def create_payout(self, receiver: str, method: VendorPaymentMethod, amount: int, fee: VendorPaymentSystem) -> None:
        """
        Withdraw money from the 5SIM vendor account.

        :param receiver: Payout receiver number
        :param method: Payment output method
        :param amount: Amount of the opyment
        :param fee: Payment executor
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
