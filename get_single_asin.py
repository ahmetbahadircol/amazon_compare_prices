from db import Mongo
from sp_api.base import Marketplaces
from sp_api.base.exceptions import SellingApiBadRequestException
from typing import Optional, Tuple

import auth_amazon
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from itertools import islice

from utils import reauth, retry_on_throttling
from sp_api.api import Products


auth_amazon.auth()
db = Mongo()
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
    breakpoint()


get_item_offers("077880206X", mp="CA")
