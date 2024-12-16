from bs4 import BeautifulSoup
import requests


def main(pgn=0):
    query = "THE BITTLEMORES (SIGNED) - Jann Arden"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&start={pgn}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    print(f"SAYFA: {pgn}")
    for result in soup.find_all("a"):
        link = result.get("href")
        if link and "/url?q=" in link:
            temp = link.split("/url?q=")[1].split("&")[0]
            if "amazon" in temp:
                print("Amazon")
                if asin := temp.split("/dp/")[-1].split("&")[0]:
                    return asin if asin else 1
    if pgn == 30:
        print("Anan")
        return
    main(pgn + 10)


print(main())
