from compare_prices.compare_prices import main as prices
from helpers.send_email import send_mail


def main():
    prices()
    send_mail()


if __name__ == "__main__":
    main()
