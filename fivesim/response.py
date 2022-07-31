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
    ru: str | None = None


class VendorWallet(NamedTuple):
    fkwallet: float
    payeer: float
    unitpay: float


class ProfileInformation(NamedTuple):
    id: int
    email: str
    vendor_name: str
    balance: float
    frozen_balance: float
    rating: float
    default_operator_name: str
    default_country: CountryInformation
    forwarding_number: str | None = None


class Payment(NamedTuple):
    id: str
    type: str
    provider: str
    amount: float
    balance: float
    created_at: datetime


class PaymentsHistory(NamedTuple):
    data: list[Payment]
    total: int
    payment_types_names: list[str] | None = None
    payment_providers_names: list[str] | None = None
    payment_statuses_names: list[str] | None = None


class SMS(NamedTuple):
    created_at: datetime
    received_at: datetime
    sender: str
    text: str
    activation_code: str
    is_wave: bool | None = None
    wave_uuid: str | None = None


class Order(NamedTuple):
    id: int
    phone: str
    created_at: datetime
    expires_at: datetime
    price: float
    status: Status
    product: ActivationProduct | HostingProduct
    operator: Operator | None = None
    country: Country | None = None
    sms: list[SMS] | None = None
    forwarding: bool | None = None
    forwarding_number: str | None = None

    @classmethod
    def from_order_id(cls, order_id: int):
        return cls(
            id=order_id,
            phone="",
            created_at=datetime.min,
            expires_at=datetime.min,
            price=0,
            status=Status.INVALID,
            product=HostingProduct.ONE_DAY
        )


class OrdersHistory(NamedTuple):
    data: list[Order]
    order_product_names: list[str]
    order_statuses_names: list[str]
    total: int
