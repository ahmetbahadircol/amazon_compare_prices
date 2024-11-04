from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

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
            self.client.admin.command("ping")
            print("Connection to MongoDB is successful.")

            self.db = self.client["amazon-compare-prices"]
            self.set_collection = self.db["books"]

        except ConnectionFailure:
            print("Connection to MongoDB failed.")
            self.client = None

    def insert_asin(self, asin: str, market_place: str) -> None:
        if self.set_collection is not None:
            result = self.set_collection.update_one(
                {"asin": asin, "market_place": market_place},
                {"$setOnInsert": {"asin": asin}},
                upsert=True,
            )

            if result.upserted_id is None:
                print(f"ASIN {asin} already exists.")
            else:
                print(f"ASIN {asin} inserted successfully.")
        else:
            print("Database connection is not established.")

    def delete_asin(self, asin: str) -> None:
        if self.set_collection:
            self.set_collection.delete_one({"asin": asin})
            print(f"ASIN {asin} deleted successfully.")
        else:
            print("Database connection is not established.")
