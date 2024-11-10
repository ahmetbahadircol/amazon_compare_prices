import pymysql
from dotenv import load_dotenv
import os

load_dotenv()


class MySQLHandler:
    def __init__(self):
        self.db_username = os.getenv("MYSQL_USER_NAME")
        self.db_pass = os.getenv("MYSQL_USER_PASS")
        self.local_db = os.getenv("USE_LOCAL_DB").lower() in [
            "true",
            "1",
            "t",
            "y",
            "yes",
        ]
        self.cursor = None
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            host=(
                "ahmetcol.mysql.pythonanywhere-services.com"
                if self.local_db
                else "localhost"
            ),
            user=self.db_username,
            password=self.db_pass,
            database="amazon_compare_prices",
        )
        self.cursor = self.connection.cursor()

    def insert(self, asin: str):
        try:
            query = f"INSERT INTO books (asin) VALUES ('{asin}')"
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                print(f"Duplicate entry found for ASIN: {asin}. Skipping.")
            else:
                raise

    def find(self, asins: list[str] = None) -> list[str]:
        # Assuming `query_conditions` is a dictionary like {'column': 'value'}
        query = f"SELECT asin FROM books"
        if asins:
            query += f" WHERE asin in {asins}"

        self.cursor.execute(query)
        asins_tuples = self.cursor.fetchall()

        return [asin[0] for asin in asins_tuples]

    def delete(self, asins: list[str]):
        # Assuming `query_conditions` is a dictionary

        query = f"DELETE FROM books WHERE asin in {asins}"
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
