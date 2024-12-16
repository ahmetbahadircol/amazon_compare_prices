from compare_prices.compare_prices import main as prices
from helpers.send_email import send_mail


def main():
    prices()
    send_mail(
        "Amazon Compare Prices TXT Files",
        ["compare_prices/buy_CA_sell_US.txt", "compare_prices/buy_US_sell_CA.txt"],
    )


if __name__ == "__main__":
    main()
