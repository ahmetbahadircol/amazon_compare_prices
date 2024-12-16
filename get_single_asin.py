from sp_api.base import Marketplaces
from typing import Optional, Tuple

from helpers.auth_amazon import auth
import time
from dotenv import load_dotenv
import os

from helpers.utils import reauth, retry_on_throttling
from sp_api.api import Products


auth()
load_dotenv()

AMAZON_SHARE = int(os.getenv("AMAZON_SHARE"))
MAX_RANK_CA = int(os.getenv("MAX_RANK_CA"))
MAX_RANK_US = int(os.getenv("MAX_RANK_US"))
USD_CA_RATE = float(os.getenv("USD_CA_RATE"))


def find_lowest_price(
    offers: list, cond: list[str] = ["new"]
) -> Tuple[Optional[float], Optional[float]]:
    if not offers:
        return None, None
    temp = list()
    for off in offers:
        try:
            if off["SubCondition"] in cond:
                list_p = off["ListingPrice"]["Amount"]
                shipping_p = off["Shipping"]["Amount"]
                temp.append(
                    (
                        list_p,
                        shipping_p,
                    )
                )
            else:
                continue
        except KeyError as e:
            print("----- KEY ERROR -----")
            print(e)
            continue

    return min(temp, key=sum)


@retry_on_throttling(delay=2, max_retries=5)
@reauth
def get_item_offers(asin: str, cond: str = "new", mp: str = "US"):
    mp_id = getattr(Marketplaces, mp)
    req = Products(marketplace=mp_id).get_item_offers(asin, cond)
    time.sleep(2)
    price, ship = find_lowest_price(req.payload["Offers"])
    print(price, ship)


if __name__ == "__main__":
    get_item_offers("0545627222", mp="CA")
