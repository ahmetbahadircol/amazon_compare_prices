import auth_amazon
from sp_api.api import Orders
from sp_api.base import Marketplaces
from datetime import datetime, timedelta
from db import Mongo
import time

auth_amazon.auth()
db = Mongo()

created_after = (
    (datetime.now() - timedelta(days=1))
    .replace(hour=0, minute=0, second=0, microsecond=0)
    .isoformat()
)


def get_asin_lists() -> Orders:
    orders_ca = (
        Orders()
        .get_orders(
            MarketplaceIds=[
                Marketplaces.CA.marketplace_id,
            ],
            CreatedAfter=created_after,
        )
        .Orders
    )
    orders_us = (
        Orders()
        .get_orders(
            CreatedAfter=created_after,
        )
        .Orders
    )

    return orders_ca + orders_us


def main() -> None:
    orders = get_asin_lists()
    order, item = None, None
    try:
        for idx, order in enumerate(orders):
            order_id = order.get("AmazonOrderId")
            sales_channel = order.get("SalesChannel")
            if sales_channel[-3:] == "com":
                market_place = "US"
            else:
                market_place = "CA"
            items = (
                Orders()
                .get_order_items(order_id=order_id)
                .payload.get("OrderItems", [])
            )
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
