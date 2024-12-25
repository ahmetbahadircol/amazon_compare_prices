from sp_api.api import ListingsRestrictions
from sp_api.base import Marketplaces
from sp_api.api import Sellers
from sp_api.api import ProductFees

from helpers.auth_amazon import auth

auth()

id = (
    ProductFees()
    .get_product_fees_estimate_for_asin(asin="0399238735", price=100.00)
    .payload["FeesEstimateResult"]["FeesEstimateIdentifier"]["SellerId"]
)
print(id)
data = {
    "asin": "0399238735",
    "sellerId": id,
    "marketplaceIds": [Marketplaces.US.marketplace_id],
}

res = ListingsRestrictions().get_listings_restrictions(**data)
print(res.payload)
