import auth_amazon
from sp_api.api import Orders
from sp_api.base import Marketplaces
from datetime import datetime, timedelta
from db import Mongo
import time

from utils import retry_on_throttling

auth_amazon.auth()
db = Mongo()

created_after = (
    (datetime.now() - timedelta(days=30))
    .replace(hour=0, minute=0, second=0, microsecond=0)
    .isoformat()
)


@retry_on_throttling(delay=1, max_retries=5)
def get_orders(market_place, created_after):
    return (
        Orders(market_place)
        .get_orders(
            CreatedAfter=created_after,
        )
        .Orders
    )


@retry_on_throttling(delay=1, max_retries=5)
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
                db.insert_asin(asin, market_place)
                print(asin + "---" + sales_channel)
            time.sleep(1)
    except KeyError as e:
        print("----- KEY ERROR ------")
        print(e)
        print(order)
        print(item)


if __name__ == "__main__":
    main()
