from db import Mongo
from sp_api.base import Marketplaces

import auth_amazon
import time

auth_amazon.auth()
db = Mongo()


from sp_api.api import Products


def get_all_asins():
    return db.find_asins()


def compare():

    books = get_all_asins()
    for book in books:
        asin, market_place = book

        book_ca = Products(marketplace=Marketplaces.CA).get_item_offers(
            asin, "new", key=Marketplaces.CA.marketplace_id
        )
        time.sleep(0.5)
        book_us = Products().get_item_offers(asin, "new")
        breakpoint()


compare()
