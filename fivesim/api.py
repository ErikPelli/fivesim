from fivesim.enums import(
    ActivationProduct,
    Category,
    Country,
    HostingProduct,
    Language,
    Operator,
    OrderAction,
    VendorPaymentMethod,
    VendorPaymentSystem
)
from fivesim.errors import ErrorType, FiveSimError
from fivesim.json_response import(
    _parse_guest_countries,
    _parse_guest_prices,
    _parse_guest_products,
    _parse_order,
    _parse_orders_history,
    _parse_payments_history,
    _parse_profile_data,
    _parse_sms_inbox
)
from fivesim.request import _APIRequest
from fivesim.response import(
    CountryInformation,
    Order,
    OrdersHistory,
    PaymentsHistory,
    ProductInformation,
    ProfileInformation,
    VendorWallet,
    SMS
)


class UserAPI(_APIRequest):
    def __init__(self, api_key: str):
        super().__init__(endpoint="https://5sim.net/v1/user/", auth_token=api_key)

    def get_profile_data(self, vendor: bool = False) -> ProfileInformation:
        """
        Get data about the user account.

        :params vendor: if true, get the vendor profile data, don't touch if you are a normal user
        :return: Profile object with the data
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path=["vendor"] if vendor else ["profile"]
        )
        return super()._parse_json(
            input=api_result,
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
            path=["orders"],
            parameters=params
        )
        return super()._parse_json(
            input=api_result,
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
            path=["payments"],
            parameters=params
        )
        return super()._parse_json(
            input=api_result,
            into_object=_parse_payments_history
        )

    def buy_number(self, country: Country, operator: Operator, product: ActivationProduct | HostingProduct, forwarding_number: str = None, reuse: bool = False, voice: bool = False) -> Order:
        """
        Buy a 5SIM number, activation or hosting.

        :param country: Target country, or ANY_COUNTRY
        :param operator: Target operator, or ANY_OPERATOR
        :param product: Product to buy
        :param forwarding_number: Only with Activation, forward the call to a russian number (11 digits, without +)
        :param reuse: Only with Activation, buy a reusable number in the future
        :param voice: Only with Activation, receive a call from a robot in the requested number
        :return: Order object
        :raises FiveSimError: if the response is invalid
        :raises ValueError: if the input parameters are invalid
        """
        params: dict[str, str] = dict()
        if isinstance(product, ActivationProduct):
            type = Category.ACTIVATION
            if forwarding_number is not None:
                if len(forwarding_number) != 11:
                    raise ValueError("Invalid forwarding number")
                params["forwarding"] = "true"
                params["number"] = forwarding_number
            if reuse:
                params["reuse"] = "1"
            if voice:
                params["voice"] = "1"
        elif isinstance(product, HostingProduct):
            type = Category.HOSTING
            if forwarding_number is not None or reuse or voice:
                raise ValueError("Parameters not supported with hosting")
        else:
            raise ValueError("Invalid product")
        api_result = super()._GET(
            use_token=True,
            path=[
                "buy",
                type.value,
                country.value,
                operator.value,
                product.value
            ],
            parameters=params
        )
        return super()._parse_json(
            input=api_result,
            into_object=_parse_order
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
            path=["reuse", product.value, number]
        )

    def order(self, action: OrderAction, order: Order) -> Order:
        """
        Apply an action to the input order.

        :param order: Order object with a valid ID, from buy_number or using from_order_id method
        :return: Parsed Order object
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path=[action.value, str(order.id)]
        )
        return super()._parse_json(
            input=api_result,
            into_object=_parse_order
        )

    def get_sms_inbox_list(self, order: Order) -> list[SMS]:
        """
        Get the list of SMS for an order ID.

        :param order: Order object with a valid ID, from buy_number or using from_order_id method
        :return: List of SMS
        :raises FiveSimError: if the response is invalid
        """
        api_result = super()._GET(
            use_token=True,
            path=["sms", "inbox", str(order.id)]
        )
        return super()._parse_json(
            input=api_result,
            into_object=_parse_sms_inbox
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
            path=["products", country.value, operator.value]
        )
        return super()._parse_json(
            input=api_result,
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
        if country != Country.ANY_COUNTRY and country is not None:
            params["country"] = country.value
        if product is not None:
            params["product"] = product.value
        api_result = super()._GET(
            use_token=False,
            path=["prices"],
            parameters=params
        )
        if api_result == "null":
            raise FiveSimError(ErrorType.INCORRECT_PRODUCT,
                               "Product isn't available for the country")
        return super()._parse_json(
            input=api_result,
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
                path=["flash", lang.value]
            )
            return super()._parse_json(input=api_result, need_keys=["text"])["text"]
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
            path=["countries"]
        )
        return super()._parse_json(
            input=api_result,
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
            path=["wallets"]
        )
        parsed = super()._parse_json(
            input=api_result,
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
            path=["orders"],
            parameters=params
        )
        return super()._parse_json(
            input=api_result,
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
            path=["payments"],
            parameters=params
        )
        return super()._parse_json(
            input=api_result,
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
        super()._POST(
            use_token=True,
            path="withdraw",
            data={
                receiver: receiver,
                method: method.value,
                amount: str(amount),
                fee: fee.value
            }
        )
