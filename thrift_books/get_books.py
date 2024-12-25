import http.client  # http.client package is used bcs requests is giving 406 error for some reason in search api
import json
from tqdm import tqdm
import os
from dotenv import load_dotenv

from compare_prices.compare_prices import get_us_and_ca_infos
from helpers.enums import BookType
from helpers.utils import get_book_type_from_asin

load_dotenv()

AMAZON_SHARE = int(os.getenv("AMAZON_SHARE"))
MAX_RANK_CA = int(os.getenv("MAX_RANK_CA"))
MAX_RANK_US = int(os.getenv("MAX_RANK_US"))
USD_CA_RATE = float(os.getenv("USD_CA_RATE"))
CATROSE_PROFIT_RATE = float(os.getenv("CATROSE_PROFIT_RATE")) + float(1)
GBOOKS_STORE_PROFIT_SHARE = int(os.getenv("GBOOKS_STORE_PROFIT_SHARE"))

MAIN_URL = "www.thriftbooks.com"


def convert_bytes_to_dict(bytes):
    string_data = bytes.decode("utf-8")
    return json.loads(string_data)


def get_asins_and_prices(page_range: int = 200):
    """
    params:

    returns:

    This function iterates 200 pages of thrift books site
    and gets the books asins and their new condition prices (each book type)
    """
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "ASP.NET_SessionId=l4whpc43lccrqtdzkqjtjplk; snow_session=3d480986-a6c3-4c3b-ac8d-0462261b851f; TIdent=5df50cdfc666417db8044b9f9decf7ba; ShowEmailSignupModal=1; osano_consentmanager_uuid=8685e9da-6056-4828-baa5-210c46c42655; osano_consentmanager=ExlS1BhD23Mll4WBji1IuhHM-Z5x2WS339w4CRS2uRmXBx_1qz_6itUI5tUD-iZL5N-TrMxIBlrkJzpa28-sDA-1Atwiiy6hKnrDwRKlWUpU-eYAVLiY2IrAvXHQCdlbI3dVfg7JSPrItoYGyHDLhp-B6HHSCmTGbYhL9Xjy0dz5NGpNnZg_v82j5RfzuD4ITNIb_OF-jJpNyDPDLXT04gOzG-AqZP1MC7E1mKfU2OMP95x3KufZpEmXyZ0FY3nzIkEec-wCrtuva76TFIRJla8EkV2D24dBk8MVN1eblpCfb30gBtbTTVEy-NO9B4anXyOHe48rrnQ=; _sp_ses.6834=*; ai_user=Tx2qnGTb1/xCk5wJEzk8H8|2024-12-23T20:17:16.755Z; CartIdentifier=cb97a55fa8cf4e9d959b340b3714a957; SessionCounter=1; showAppBanner=1; ShownEmailSignupBanner=1; _gcl_au=1.1.1885813053.1734985037; ab.storage.deviceId.9b697b56-3ad5-4d70-afb3-6bf89f582a03=%7B%22g%22%3A%2278e47fc9-214c-2325-a98c-3fe01121db33%22%2C%22c%22%3A1734985037086%2C%22l%22%3A1734985037086%7D; _gid=GA1.2.730244685.1734985037; _clck=eiwgn4%7C2%7Cfry%7C0%7C1818; _pin_unauth=dWlkPVpXVmtOakpqT0RrdFpqbGtOQzAwTVdWaUxXRTBNVEF0WW1GaFptUTBNbVJoWVRFMg; sp=d9af315a-73ea-444f-a8f8-466a78f6c9ad; UserDataIdentifier=d2555d8d1f93495081af3a85c2c5a0bd; tbs=824071592; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22j2HqVMAYI7PiUe7la1eh%22%2C%22expiryDate%22%3A%222025-12-23T20%3A48%3A07.810Z%22%7D; _rdt_uuid=1734985037259.8597a771-f055-4c44-850c-c31ed7e4d706; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A0%2C%22expiryDate%22%3A%222025-12-23T20%3A48%3A07.917Z%22%7D; _uetsid=e7f79d70c16a11ef978c65da496f7afc; _uetvid=e7f7d590c16a11ef8b95973e2a3d9b80; ab.storage.sessionId.9b697b56-3ad5-4d70-afb3-6bf89f582a03=%7B%22g%22%3A%22d07f2976-3ebd-37cf-570c-b373cb6b2d45%22%2C%22e%22%3A1734988687951%2C%22c%22%3A1734985037085%2C%22l%22%3A1734986887951%7D; _ga=GA1.2.536527661.1734985037; cto_bundle=ej7TsF8zOWY1b0UlMkJpMU9ZcnElMkY1NFRBeXZtWXpXcXdqV25zTlNYSWxjbUVleUJ2N0FZbGNXbUp1ZXlBdVNXWmt1T3YlMkY3SFBwbWpJSHRHUlo1SEoyWFRIJTJGVkRrb2ZBS0RlSE1kVzZ6bW94Y1FyanhQQ1JFN0VLbmtLazdtQ0RhMGtrcFBsVkxVVyUyQkZTbFElMkZxd2NMYWJXaVVRb1NaTllJMXdvTlBYcmVtJTJCdk1DNVh3dHVBVWxNdVVCOFFEUlJLQUpYbFdzaDAwckZJb3AyNDE1bXFwTnlFM1hFN2clM0QlM0Q; _clsk=1uyg9mh%7C1734986888373%7C10%7C0%7Cw.clarity.ms%2Fcollect; _sp_id.6834=bfd8e9a1-2f5f-4d7b-a071-cbed1d09f9d8.1734985037.1.1734986919.1734985037.27ed5af5-f487-47e1-8631-043a84bda2d8; _ga_T0W870EHBL=GS1.1.1734985037.1.1.1734986919.60.0.0; ai_session=ZEqdAPsQIbQ1qny+PpfxqT|1734985037157|1734986919168; ASP.NET_SessionId=5z4bo2cz4w5seegjnpkxmrm2; CartIdentifier=8d319d17e510404ca1bea4e811f713a8; TIdent=5df50cdfc666417db8044b9f9decf7ba",
        "Origin": "https://www.thriftbooks.com",
        "Referer": "https://www.thriftbooks.com/browse/",
        "Request-Id": "|b1099725a7054b61a20b8bf47bd0376c.6c98ec0cbb724178",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "traceparent": "00-b1099725a7054b61a20b8bf47bd0376c-6c98ec0cbb724178-01",
    }
    result = dict()
    for page in range(1, page_range + 1):
        try:
            conn = http.client.HTTPSConnection(MAIN_URL)
            payload = json.dumps(
                {
                    "searchTerms": [""],
                    "sortBy": "bestsellers",
                    "sortDirection": "desc",
                    "page": str(page),
                    "itemsPerPage": "50",
                    "displayType": 0,
                    "maxPrice": "10",
                    "isInStock": True,
                    "idproducttype": "1",
                    "media": [45, 74],
                    "quality": [1],
                    "currentPage": "200",
                    "resultsPerPage": "50",
                }
            )
            conn.request("POST", "/api/browse/Search", payload, headers)
            res = conn.getresponse()
            if res.status != 200:
                print(f"Sometihng is wrong in Search Page: {page}!")
                continue
            data = res.read()
            books = convert_bytes_to_dict(data)["works"]
            print("Thrift Books store got Search Page!")
            for book in tqdm(books, desc=f"Sending Request on Page: {page}"):
                dict1, dict2 = dict(), dict()
                try:
                    conn = http.client.HTTPSConnection(MAIN_URL)
                    id_iq = book["idIq"]
                    id_work = book["idWork"]
                    id_amazon = book["idAmazon"]
                    payload = json.dumps({"workId": id_work, "IdAmazon": id_amazon})
                    conn.request(
                        "POST",
                        "/stateless/editions/workinfo",
                        payload,
                        headers=headers,
                    )
                    deteail_res = conn.getresponse()
                    if deteail_res.status != 200:
                        print(
                            f"Sometihng is wrong with workID: {id_work} and IdIq: {id_iq}"
                        )
                        continue
                    data = convert_bytes_to_dict(deteail_res.read())["Work"]
                    """
                    ActiveEdition has media type (paper or hard) and there are Copies
                    property of this media type. The condition new price here.
                    And the other book type is in PopularEditions part. Find the related
                    book type here. For example if ActiveEdition is paper, find the hardcover in
                    editioninfo api. And there is do the same logic there, too.
                    if whether paper or hardcover is has New condition price, add the result.
                    """
                    dict1["type"] = (
                        data["ActiveEdition"]["Media"]
                        if [v.value for v in BookType]
                        else None
                    )
                    if dict1["type"]:
                        dict1["title"] = data["Title"]
                        dict1["asin"] = data["ActiveEdition"]["ISBN"]
                        # Iterate copies property
                        for copy in data["ActiveEdition"]["Copies"]:
                            if copy["Quality"] == "New":
                                dict1["price"] = float(copy["Price"])

                    if dict1["type"]:
                        dict2["type"] = (
                            BookType.HARD.value
                            if dict1["type"] == BookType.PAPER.value
                            else BookType.PAPER.value
                        )
                    else:
                        dict2["type"] = None
                    # Find other book type in editions/editioninfo api
                    if dict2["type"]:
                        dict2["title"] = data["Title"]
                        id_amazon2 = None
                        for edition in data["PopularEditions"]:
                            if edition["Title"] == dict2["type"]:
                                id_amazon2 = edition["IdAmazon"]
                        if id_amazon2 is None:
                            continue
                        conn.request(
                            "POST",
                            "/api/editions/editioninfo",
                            json.dumps({"idAmazon": id_amazon2}),
                            headers=headers,
                        )
                        deteail_res2 = conn.getresponse()
                        if deteail_res2.status != 200:
                            print(
                                f"Sometihng is wrong with workID: {id_work} and IdIq: {id_iq}"
                            )
                            continue
                        data2 = convert_bytes_to_dict(deteail_res2.read())["Edition"]
                        dict2["asin"] = data2["ISBN"]
                        for copy in data2["Copies"]:
                            if copy["Quality"] == "New":
                                dict2["price"] = float(copy["Price"])

                    if dict1.get("price"):
                        result[dict1["asin"]] = dict1
                    if dict2.get("price"):
                        result[dict2["asin"]] = dict2
                finally:
                    conn.close()

        finally:
            conn.close()

    return result


def compare_thrift_store_amazon(thrift_books_info: dict):
    amazon_ca_infos, amazon_us_infos = get_us_and_ca_infos(thrift_books_info.keys())
    for asin, thrift_book_info in thrift_books_info.items():
        tb_title, tb_price, tb_type = (
            thrift_book_info.get("title"),
            thrift_book_info.get("price"),
            thrift_book_info.get("type"),
        )
        amazon_info_ca = amazon_ca_infos.get(asin)
        amazon_info_us = amazon_us_infos.get(asin)
        if not amazon_info_ca or not amazon_info_us:
            continue
        
        amazon_lowest_price_ca = amazon_info_ca["list_price"]
        amazon_rank_ca = amazon_info_ca["rank"]
        amazon_lowest_price_us = round(
            amazon_info_us["list_price"] * USD_CA_RATE, 2
        )  # CONVERT TO CAD
        amazon_rank_us = amazon_info_us["rank"]
        amazon_book_type = get_book_type_from_asin(asin)

        if tb_type != amazon_book_type:
            continue

        # Sell at Canada
        if amazon_lowest_price_ca > amazon_lowest_price_us:
            if all(
                [
                    (tb_price + GBOOKS_STORE_PROFIT_SHARE) < amazon_lowest_price_ca,
                    amazon_rank_ca < MAX_RANK_CA,
                ]
            ):
                print(f"ADDED {asin} in CA file")
                with open(f"thrift_books/sell_CA.txt", "a") as file_ca:
                    file_ca.write(
                        f"{tb_title}\t{tb_price}\t{amazon_rank_ca}\t{amazon_lowest_price_ca}\n"
                    )
        else:  # Sell at US
            if all(
                [
                    (tb_price + GBOOKS_STORE_PROFIT_SHARE) < amazon_lowest_price_us,
                    amazon_rank_us < MAX_RANK_US,
                ]
            ):
                print(f"ADDED {asin} in US file")
                with open(f"gbook_store/sell_US.txt", "a") as file_us:
                    file_us.write(
                        f"{tb_title}\t{tb_price}\t{amazon_rank_us}\t{amazon_lowest_price_us}\n"
                    )


def create_txt():
    with open(f"thrift_books/sell_CA.txt", "w") as file_ca:
        file_ca.write(
            f"TITLE  |  TB-STORE-PRICE(CAD)  |  RANK CA  |  AMAZON CA PRICE\n-----------------------------------------\n"
        )
    with open(f"thrift_books/sell_US.txt", "w") as file_us:
        file_us.write(
            f"TITLE  |  TB-STORE-PRICE(CAD)  |  RANK US  |  AMAZON US PRICE\n-----------------------------------------\n"
        )
