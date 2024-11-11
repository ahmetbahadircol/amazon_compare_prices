from db import MySQLHandler
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

auth_amazon.auth()
db = MySQLHandler()
load_dotenv()

AMAZON_SHARE = int(os.getenv("AMAZON_SHARE"))
MAX_RANK_CA = int(os.getenv("MAX_RANK_CA"))
MAX_RANK_US = int(os.getenv("MAX_RANK_US"))
USD_CA_RATE = float(os.getenv("USD_CA_RATE"))
CATROSE_PROFIT_RATE = float(os.getenv("CATROSE_PROFIT_RATE")) + float(1)


from sp_api.api import Products


@retry_on_throttling(delay=2, max_retries=5)
@reauth
def get_all_asins() -> list[str]:
    """
    returns list of asin numbers of books
    """
    return db.find()


def format_time(t):
    return (
        datetime.fromtimestamp(t).strftime("%H:%M:%S") + f":{int((t % 1) * 1000):03d}"
    )


def create_txt():
    with open(f"buy_CA_sell_US.txt", "w") as file_ca:
        file_ca.write(
            f"ASIN  |  US PRICE(CAD)  |  RANK CA  |  CA PRICE\n-----------------------------------------\n"
        )
    with open(f"buy_US_sell_CA.txt", "w") as file_us:
        file_us.write(
            f"ASIN  |  US PRICE(CAD)  |  RANK CA  |  CA PRICE\n-----------------------------------------\n"
        )


@retry_on_throttling(delay=2, max_retries=7)
@reauth
def get_offers_batch(market_place: str, asins: list[str]) -> list[dict]:
    """
    returns list of offers for each book

    TODO: Make this fucntion for flexibile item condition: [new, used, ...]
    """
    requests = []
    for asin in asins:
        request = {
            "uri": f"/products/pricing/v0/items/{asin}/offers",
            "method": "GET",
            "ItemCondition": "New",
            "MarketplaceId": getattr(Marketplaces, market_place).marketplace_id,
        }
        requests.append(request)
    try:
        res = Products().get_item_offers_batch(requests).payload["responses"]
        time.sleep(2.01)
        return res
    except SellingApiBadRequestException as e:
        print(e)


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


def compare(books) -> None:
    """
    returns None

    This function has three main parts:
        1. get asin, rank, price, and shipping price of the books (each market) and save it into a dict
        2. compare for each asin(book)'s price and ranks and decide "SHOULD BUYs" and "SHOULD SELLs"
        3. Write them into the txt files
    """
    books_ca = get_offers_batch("CA", books)
    books_us = get_offers_batch("US", books)
    book_info_us, book_info_ca = dict(), dict()
    for book in books_us:
        try:
            list_price, shipping_price = find_lowest_price(
                book["body"]["payload"]["Offers"]
            )
            if list_price is not None or shipping_price is not None:
                book_info_us[book["body"]["payload"]["ASIN"]] = {
                    "rank": book["body"]["payload"]["Summary"]["SalesRankings"][0][
                        "Rank"
                    ],
                    "list_price": list_price,
                    "shipping_price": shipping_price,
                }
        except KeyError as e:
            print("----- KEY ERROR -----")
            print(e)
            continue

    for book in books_ca:
        try:
            list_price, shipping_price = find_lowest_price(
                book["body"]["payload"]["Offers"]
            )
            if list_price is not None or shipping_price is not None:
                book_info_ca[book["body"]["payload"]["ASIN"]] = {
                    "rank": book["body"]["payload"]["Summary"]["SalesRankings"][0][
                        "Rank"
                    ],
                    "list_price": list_price,
                    "shipping_price": shipping_price,
                }
        except KeyError as e:
            print("----- KEY ERROR -----")
            print(e)
            continue

    for asin, info_ca in book_info_ca.items():
        info_us = book_info_us.get(asin)
        if not info_us:
            continue

        lowest_price_ca = info_ca["list_price"]
        shipping_price_ca = info_ca["shipping_price"]
        rank_ca = info_ca["rank"]
        lowest_price_us = round(info_us["list_price"] * USD_CA_RATE, 2)
        shipping_price_us = round(
            info_us["shipping_price"] * USD_CA_RATE, 2
        )  # CONVERT TO CAD
        rank_us = info_us["rank"]

        # Compare Canada and US

        # Buy from Canada and Sell in US
        if all(
            [
                rank_us < MAX_RANK_US,
                (lowest_price_ca + shipping_price_ca) * CATROSE_PROFIT_RATE
                + AMAZON_SHARE
                < lowest_price_us,
            ]
        ):
            print(f"ADDED {asin} in US file")
            with open(f"buy_CA_sell_US.txt", "a") as file_us:
                file_us.write(
                    f"{asin}\t{lowest_price_us}\t{rank_us}\t{lowest_price_ca}\n"
                )

        # Buy from US and Sell in Canada
        if all(
            [
                rank_ca < MAX_RANK_CA,
                (lowest_price_us + shipping_price_us) * CATROSE_PROFIT_RATE
                + AMAZON_SHARE
                < lowest_price_ca,
            ]
        ):
            print(f"ADDED {asin} in CA file")
            with open(f"buy_US_sell_CA.txt", "a") as file_ca:
                file_ca.write(
                    f"{asin}\t{lowest_price_us}\t{rank_ca}\t{lowest_price_ca}\n"
                )

    print("Data written to output.txt")


def chunk_list(data, chunk_size=20):
    for i in range(0, len(data), chunk_size):
        yield list(islice(data, i, i + chunk_size))


def main():
    create_txt()
    all_books = get_all_asins()
    test = 1
    for chunk in chunk_list(all_books):
        print(f"{test}. try: ")
        compare(chunk)
        test += 1


if __name__ == "__main__":
    main()
