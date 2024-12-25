from helpers.send_email import send_mail
from helpers.utils import chunk_dict
from thrift_books.get_books import (
    compare_thrift_store_amazon,
    create_txt,
    get_asins_and_prices,
)


def main():
    res = get_asins_and_prices(1)
    if res:
        for chunk in chunk_dict(res):
            # TODO: If there is nothing in txt files, don't call send_email
            create_txt()
            compare_thrift_store_amazon(chunk)
            send_mail(
                subject="Thrift Books Store",
                attachments=["thrift_books/sell_CA.txt", "thrift_books/sell_US.txt"],
            )
    else:
        print("There is nothing to send!")


if __name__ == "__main__":
    main()
