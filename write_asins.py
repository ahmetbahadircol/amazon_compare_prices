from sp_api.api import Orders
from sp_api.base import Marketplaces
from datetime import datetime, timedelta
from helpers import auth_amazon
from helpers.db import MySQLHandler
import time
from dotenv import load_dotenv
import os

from helpers.utils import reauth, retry_on_throttling

auth_amazon.auth()
db = MySQLHandler()
load_dotenv()

PULL_DAYS_ASIN = int(os.getenv("PULL_DAYS_ASIN"))

created_after = (
    (datetime.now() - timedelta(days=PULL_DAYS_ASIN))
    .replace(hour=0, minute=0, second=0, microsecond=0)
    .isoformat()
)


@retry_on_throttling(delay=1, max_retries=10)
@reauth
def get_orders(market_place, created_after, orders_list=None, next_token=None):
    if orders_list is None:
        orders_list = []
    if next_token:
        response = Orders(market_place).get_orders(NextToken=next_token)
    else:
        response = Orders(market_place).get_orders(CreatedAfter=created_after)

    orders_list.extend(response.payload.get("Orders", []))

    next_token = response.payload.get("NextToken")

    if next_token:
        return get_orders(market_place, created_after, orders_list, next_token)
    else:
        return orders_list


@retry_on_throttling(delay=1, max_retries=5)
@reauth
def get_items(order_id):
    return Orders().get_order_items(order_id=order_id).payload.get("OrderItems", [])


def main() -> None:
    orders = get_orders(Marketplaces.CA, created_after) + get_orders(
        Marketplaces.US, created_after
    )
    order, item = None, None
    try:
        for idx, order in enumerate(orders):
            order_id = order.get("AmazonOrderId")
            sales_channel = order.get("SalesChannel")
            if sales_channel[-3:] == "com":
                market_place = "US"
            else:
                market_place = "CA"
            items = get_items(order_id)
            for item in items:
                asin = item.get("ASIN")
                db.insert(asin)
                print(asin + "---" + sales_channel)
            time.sleep(1)
    except KeyError as e:
        print("----- KEY ERROR ------")
        print(e)
        print(order)
        print(item)


if __name__ == "__main__":
    main()
