from fivesim.order import ActivationProduct, Country, HostingProduct, Product
from typing import Any, NamedTuple


class ProductInformation(NamedTuple):
    category: str
    quantity: int
    price: int


def _parse_products(input: dict[str, dict[str, Any]]) -> Any:
    if "Category" in input:
        return ProductInformation(
            category=input["Category"],
            quantity=input["Qty"] if "Qty" in input else 0,
            price=input["Price"] if "Price" in input else 0
        )
    else:
        result: dict[ActivationProduct |
                     HostingProduct, ProductInformation] = dict()
        for key, value in input.items():
            try:
                if value.category == "activation":
                    result[ActivationProduct(key)] = value
                elif value.category == "hosting":
                    result[HostingProduct(key)] = value
            except:
                pass
        return result


class CountryInformation(NamedTuple):
    iso: str
    prefix: str
    en: str
    ru: str


def _parse_countries(input: dict[str, dict[str, Any]]) -> Any:
    if "iso" in input:
        return CountryInformation(
            iso=next(iter(input["iso"])),
            prefix=next(iter(input["prefix"])),
            en=input["text_en"],
            ru=input["text_ru"],
        )
    elif len(input) > 0 and isinstance(next(iter(input)), CountryInformation):
        result: dict[Country, CountryInformation] = dict()
        for key, value in input.items():
            try:
                result[Country(key)] = value
            except:
                pass
        return result
    else:
        return input
