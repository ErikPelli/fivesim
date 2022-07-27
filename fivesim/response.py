from datetime import datetime
from fivesim.order import(
    ActivationProduct,
    Category,
    Country,
    HostingProduct,
    Operator,
    Status
)
from typing import Any, NamedTuple


class ProductInformation(NamedTuple):
    category: Category
    quantity: int
    price: float


def _parse_guest_products(input: dict[str, dict[str, Any]]) -> Any:
    if "Category" in input:
        return ProductInformation(
            category=Category(input["Category"]),
            quantity=input["Qty"] if "Qty" in input else 0,
            price=input["Price"] if "Price" in input else 0
        )
    else:
        result: dict[ActivationProduct |
                     HostingProduct, ProductInformation] = dict()
        for key, value in input.items():
            try:
                if value.category == Category.ACTIVATION:
                    result[ActivationProduct(key)] = value
                elif value.category == Category.HOSTING:
                    result[HostingProduct(key)] = value
            except:
                pass
        return result


def _parse_guest_prices(input: dict[str, dict[str, Any]]) -> Any:
    if len(input) > 0:
        if "count" in input:
            return ProductInformation(
                category=Category.ACTIVATION,
                quantity=input["count"],
                price=input["cost"]
            )

        result = dict()
        hasProductInformation = isinstance(
            next(iter(input.values())), ProductInformation
        )
        if not hasProductInformation:
            # Get the first key of the first element, which is a dict
            keyOfChildDictionary = next(
                iter(next(iter(input.values())).keys())
            )

        for key, value in input.items():
            try:
                if hasProductInformation:
                    result[Operator(key)] = value
                elif isinstance(keyOfChildDictionary, Operator):
                    try:
                        result[Country(key)] = value
                    except:
                        result[ActivationProduct(key)] = value
                elif isinstance(keyOfChildDictionary, Country):
                    for key2, value2 in value.items():
                        try:
                            result[key2] = {ActivationProduct(key): value2}
                        except:
                            pass
                elif isinstance(keyOfChildDictionary, ActivationProduct):
                    result[Country(key)] = value
                else:
                    break
            except:
                pass
        else:
            return result
    return input


class CountryInformation(NamedTuple):
    iso: str
    prefix: str
    en: str
    ru: str


def _parse_guest_countries(input: dict[str, dict[str, Any]]) -> Any:
    if "iso" in input:
        return CountryInformation(
            iso=next(iter(input["iso"])),
            prefix=next(iter(input["prefix"])),
            en=input["text_en"],
            ru=input["text_ru"],
        )
    elif len(input) > 0 and isinstance(next(iter(input.values())), CountryInformation):
        result: dict[Country, CountryInformation] = dict()
        for key, value in input.items():
            try:
                result[Country(key)] = value
            except:
                pass
        return result
    else:
        return input


class VendorWallet(NamedTuple):
    fkwallet: float
    payeer: float
    unitpay: float


class ProfileInformation(NamedTuple):
    id: int
    email: str
    vendor_name: str
    forwarding_number: str
    balance: float
    frozen_balance: float
    rating: float
    default_operator_name: str
    default_country: CountryInformation


def _parse_profile_data(input: dict[str, dict[str, Any]]) -> Any:
    if "iso" in input:
        return CountryInformation(
            iso=input["iso"],
            prefix=input["prefix"],
            en=input["name"],
            ru=input["name"],
        )
    elif "name" in input:
        return input
    else:
        return ProfileInformation(
            id=input["id"],
            email=input["email"],
            vendor_name=input["vendor"],
            forwarding_number=input["default_forwarding_number"],
            balance=input["balance"],
            frozen_balance=input["frozen_balance"],
            rating=input["rating"],
            default_operator_name=input["default_operator"]["name"],
            default_country=input["default_country"]
        )


class Payment(NamedTuple):
    id: str
    type: str
    provider: str
    amount: float
    balance: float
    created_at: datetime


class PaymentsHistory(NamedTuple):
    data: list[Payment]
    payment_types_names: list[str] | None
    payment_providers_names: list[str] | None
    payment_statuses_names: list[str] | None
    total: int


def _parse_payments_history(input: dict[str, dict[str, Any]]) -> Any:
    if "Name" in input:
        return input["Name"]
    elif "ID" in input:
        return Payment(
            id=input["ID"],
            type=input["TypeName"],
            provider=input["ProviderName"],
            amount=input["Amount"],
            balance=input["Balance"],
            created_at=datetime.fromisoformat(input["CreatedAt"]),
        )
    else:
        return PaymentsHistory(
            data=input["Data"],
            payment_types_names=input["PaymentTypes"],
            payment_providers_names=input["PaymentProviders"],
            payment_statuses_names=input["PaymentStatuses"] if "PaymentStatuses" in input else None,
            total=input["Total"]
        )


class SMS(NamedTuple):
    id: int
    created_at: datetime
    received_at: datetime
    sender: str
    text: str
    activation_code: str
    is_wave: bool | None
    wave_uuid: str | None


class Order(NamedTuple):
    id: int
    phone: str
    created_at: datetime
    expires_at: datetime
    operator: Operator | None
    product: ActivationProduct | HostingProduct
    country: Country | None
    price: float
    status: Status
    sms: SMS | None
    forwarding: bool | None
    forwarding_number: str | None


class OrdersHistory(NamedTuple):
    data: list[Order]
    order_product_names: list[str]
    order_statuses_names: list[str]
    total: int


def _parse_sms(input: dict[str, dict[str, Any]]) -> Any:
    return SMS(
        id=input["id"] if "id" in input else input["ID"],
        created_at=datetime.fromisoformat(input["created_at"]),
        received_at=datetime.fromisoformat(input["date"]),
        sender=input["sender"],
        text=input["text"],
        activation_code=input["code"],
        is_wave=input["is_wave"] if "is_wave" in input else None,
        wave_uuid=input["wave_uuid"] if "wave_uuid" in input else None
    )


def _parse_order(input: dict[str, dict[str, Any]]) -> Any:
    try:
        product = ActivationProduct(input["product"])
    except:
        try:
            product = HostingProduct(input["product"])
        except:
            product = None
    return Order(
        id=input["id"],
        phone=input["phone"],
        created_at=datetime.fromisoformat(input["created_at"]),
        expires_at=datetime.fromisoformat(input["expires"]),
        operator=input["operator"] if "operator" in input else None,
        product=product,
        country=Country(input["phone"]) if "country" in input else None,
        price=input["price"],
        status=Status.from_status_string(input["status"]),
        sms=input["sms"],
        forwarding=input["forwarding"] if "forwarding" in input else None,
        forwarding_number=input["forwarding_number"] if "forwarding_number" in input else None,
    )


def _parse_orders_history(input: dict[str, dict[str, Any]]) -> Any:
    if any(i in input for i in ["Name", "name"]):
        return input["Name"] if "Name" in input else input["name"]
    elif "text" in input:
        return _parse_sms(input)
    elif "phone" in input:
        return _parse_order(input)
    else:
        return OrdersHistory(
            data=input["Data"],
            order_product_names=input["ProductNames"],
            order_statuses_names=input["Statuses"],
            total=input["Total"]
        )
