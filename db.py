from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os
from utils import ensure_collection

load_dotenv()


class Mongo:
    def __init__(self):
        self.db_username = os.getenv("MONGODB_USER_NAME")
        self.db_pass = os.getenv("MONGODB_USER_PASS")
        self.client = None
        self.db = None
        self.set_collection = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(
                f"mongodb+srv://{self.db_username}:{self.db_pass}@amazon-compare-prices.jg8xs.mongodb.net/amazon-compare-prices?retryWrites=true&w=majority"
            )
            # breakpoint()
            self.client.admin.command("ping")
            print("Connection to MongoDB is successful.")

            self.db = self.client["amazon-compare-prices"]
            self.set_collection = self.db["books"]

        except ConnectionFailure as e:
            print("Connection to MongoDB failed.")
            raise e

    @ensure_collection
    def insert_asin(self, asin: str, market_place: str) -> None:
        result = self.set_collection.update_one(
            {"asin": asin, "market_place": market_place},
            {"$setOnInsert": {"asin": asin}},
            upsert=True,
        )

        if result.upserted_id is None:
            print(f"ASIN {asin} already exists.")
        else:
            print(f"ASIN {asin} inserted successfully.")

    @ensure_collection
    def delete_asin(self, asin: str) -> None:
        self.set_collection.delete_one({"asin": asin})
        print(f"ASIN {asin} deleted successfully.")

    @ensure_collection
    def find_asins(self, asins: list[str] = None) -> list[tuple]:
        projection = {"_id": 0, "asin": 1, "market_place": 1}
        if asins:
            res = self.set_collection.find({"asin": {"$in": asins}}, projection)
        else:

            res = self.set_collection.find({}, projection)

        asin_list = [(doc["asin"], doc["market_place"]) for doc in res]

        return asin_list
