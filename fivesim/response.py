from fivesim.order import ActivationProduct, HostingProduct, Product
from typing import Any, NamedTuple


class ProductInformation(NamedTuple):
    Qty: int
    Price: int


def _parse_products(input: dict[str, dict[str, Any]]) -> dict[Product, ProductInformation]:
    result: dict[Product, ProductInformation] = dict()
    for key, value in input.items():
        try:
            if value["Category"] == "activation":
                newKey = ActivationProduct(key)
            elif value["Category"] == "hosting":
                newKey = HostingProduct(key)
            else:
                raise ValueError
        except ValueError:
            continue

        result[newKey] = ProductInformation(
            Qty=value["Qty"] if "Qty" in value else 0,
            Price=value["Price"] if "Price" in value else 0
        )
