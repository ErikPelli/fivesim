from fivesim.order import(
    ActivationProduct,
    Category,
    Country,
    HostingProduct,
    Operator
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


class VendorProfile(NamedTuple):
    id: int
    email: str
    vendor_name: str
    forwarding_number: str
    balance: float
    frozen_balance: float
    rating: float
    default_operator_name: str
    default_country: CountryInformation


def _parse_vendor_data(input: dict[str, dict[str, Any]]) -> Any:
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
        return VendorProfile(
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
