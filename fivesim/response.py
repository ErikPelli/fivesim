from datetime import datetime
from fivesim.enums import(
    ActivationProduct,
    Category,
    Country,
    HostingProduct,
    Operator,
    Status
)
from typing import NamedTuple


class ProductInformation(NamedTuple):
    category: Category
    quantity: int
    price: float


class CountryInformation(NamedTuple):
    iso: str
    prefix: str
    en: str
    ru: str | None


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
    sms: list[SMS] | None
    forwarding: bool | None
    forwarding_number: str | None

    @classmethod
    def from_order_id(cls, order_id: int):
        return cls(id=order_id)


class OrdersHistory(NamedTuple):
    data: list[Order]
    order_product_names: list[str]
    order_statuses_names: list[str]
    total: int
