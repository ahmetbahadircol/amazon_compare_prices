from db import Mongo
from sp_api.base import Marketplaces
from sp_api.base.exceptions import SellingApiBadRequestException

import auth_amazon
import time
from datetime import datetime
from dotenv import load_dotenv
import os

from utils import retry_on_throttling

auth_amazon.auth()
db = Mongo()
load_dotenv()

AMAZON_SHARE = int(os.getenv("AMAZON_SHARE"))
MAX_RANK_CA = int(os.getenv("MAX_RANK_CA"))
MAX_RANK_US = int(os.getenv("MAX_RANK_US"))
USD_CA_RATE = float(os.getenv("USD_CA_RATE"))


from sp_api.api import Products


@retry_on_throttling(delay=2, max_retries=5)
def get_all_asins():
    return db.find_asins()


@retry_on_throttling(delay=2, max_retries=5)
def get_offers(market_place: str, asin: str):
    try:
        return Products(marketplace=market_place).get_item_offers(asin, "new")
    except SellingApiBadRequestException as e:
        print(e)


@retry_on_throttling(delay=2, max_retries=5)
def format_time(t):
    return (
        datetime.fromtimestamp(t).strftime("%H:%M:%S") + f":{int((t % 1) * 1000):03d}"
    )


def create_txt():
    with open(f"output_CA.txt", "w") as file_ca:
        pass
    with open(f"output_US.txt", "w") as file_us:
        pass


def compare():
    books = get_all_asins()
    # books = [("B06XF42YJD", "")]
    create_txt()
    for book in books:
        asin, market_place = book
        book_ca = get_offers(Marketplaces.CA, asin)
        time.sleep(2)
        book_us = get_offers(Marketplaces.US, asin)
        time.sleep(2)
        lowest_price_ca, lowest_price_us = None, None

        try:
            # Canada Lowest Price
            offers_ca = book_ca.payload["Summary"]["LowestPrices"]
            for offer in offers_ca:
                if offer["condition"] == "new":
                    lowest_price_ca = offer["LandedPrice"]["Amount"]
                    break
            rank_ca = book_ca.payload["Summary"]["SalesRankings"][0]["Rank"]

            # US Lowest Prices
            offers_us = book_us.payload["Summary"]["LowestPrices"]
            for offer in offers_us:
                if offer["condition"] == "new":
                    lowest_price_us = round(
                        offer["LandedPrice"]["Amount"] * USD_CA_RATE, 2
                    )
                    break
            rank_us = book_us.payload["Summary"]["SalesRankings"][0]["Rank"]

        except KeyError as e:
            print("----- KEY ERROR ------")
            print(e)
            print(offers_us)
            print(offers_us)
            continue

        except AttributeError as e:
            print(e)
            continue

        if None in [lowest_price_ca, rank_ca, lowest_price_us, rank_us]:
            print("----- PRICE ERROR ------")
            print(lowest_price_ca, rank_ca, lowest_price_us, rank_us)
            continue

        print(
            lowest_price_ca,
            rank_ca,
            lowest_price_us,
            rank_us,
            f"arasındaki fark: {round(abs(lowest_price_ca - lowest_price_us),2)}",
        )

        # Compare Canada and US

        # Buy from Canada and Sell in US
        if lowest_price_ca < lowest_price_us:
            if all(
                [
                    rank_us < MAX_RANK_US,
                    lowest_price_ca + AMAZON_SHARE < lowest_price_us,
                ]
            ):
                print(f"ADDED {asin} in US file")
                with open(f"output_US.txt", "a") as file:
                    file.write(
                        f"{asin}\t{lowest_price_us}\t{rank_us}\t{lowest_price_ca}\n"
                    )

        # Buy from US and Sell in Canada
        else:
            if all(
                [
                    rank_ca < MAX_RANK_CA,
                    lowest_price_us + AMAZON_SHARE < lowest_price_ca,
                ]
            ):
                print(f"ADDED {asin} in CA file")
                with open(f"output_CA.txt", "a") as file:
                    file.write(
                        f"{asin}\t{lowest_price_us}\t{rank_ca}\t{lowest_price_ca}\n"
                    )

    print("Data written to output.txt")


compare()
