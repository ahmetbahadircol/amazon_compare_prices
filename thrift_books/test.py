import http.client # http.client package is used bcs requests is giving 406 error for some reason
import json


def anan():

    conn = http.client.HTTPSConnection("www.thriftbooks.com")
    payload = json.dumps(
        {
            "searchTerms": [""],
            "sortBy": "bestsellers",
            "sortDirection": "desc",
            "page": "200",
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
    conn.request("POST", "/api/browse/Search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
