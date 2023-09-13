from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup
from pony import orm

db = orm.Database()
db.bind(provider='sqlite', filename='items.db', create_db=True)


class Item(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_date = orm.Required(datetime)


db.generate_mapping(create_tables=True)

from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
import re


def export_data_to_csv():
    data = Item.select_by_sql("SELECT * FROM Price")
    for d in data:
        print(d)


def courtOrder(session):
    price_float = 0.0
    url = "https://courtorder.co.za/products/air-force-1-low-white-8?currency=ZAR&variant=43637683355797&utm_medium" \
          "=cpc&utm_source=google&utm_campaign=Google%20Shopping&stkn=b54420df916d&gclid" \
          "=Cj0KCQjwmICoBhDxARIsABXkXlJ_yo10nVnYCUlVvVBqM4QFhcw26M-xNzbHU1WfbsN4osG9DSWJQdEaArEWEALw_wcB"

    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all the price elements
    price_elements = soup.select("span.product__price")

    # Initialize an empty list to store the cleaned prices
    cleaned_prices = []

    for price_element in price_elements:
        price_text = price_element.text.strip()  # Remove leading/trailing whitespace

        # Extract the price value (before the slash) using regular expressions
        price_match = re.match(r'^([^/]+)', price_text)
        if price_match:
            cleaned_prices.append(price_match.group(1))

    if cleaned_prices:
        # Take the first cleaned price (if available)
        sub1 = 'R'
        sub2 = "\n"
        newstr = cleaned_prices[0]
        index1 = newstr.find(sub1)
        index2 = newstr.find(sub2)
        res = newstr[index1 + len(sub1) + 1: index2]
        res = res.replace(',', '')
        price_float = float(res)
    else:
        price_text = "Price not found"

    data = ("Court Order", price_float)
    return data


def superbalist(session):
    price_float = 0.0
    url = "https://superbalist.com/women/shoes/sneakers/air-force-1-07-dd8959-100-white-white-white-white/718795" \
          "?clickRef=catalogue"

    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all the price elements
    price_elements = soup.select_one("span.price").text.replace("R", "").strip()

    # Initialize an empty list to store the cleaned prices
    cleaned_prices = []

    price_float = float(price_elements)

    data = ("Superbalist", price_float)
    return data


def studio88(session):
    price_float = 0.0
    url = "https://www.studio-88.co.za/nike-air-force-1-07-mens-white"

    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all the price elements
    price_elements = soup.select_one("span.price").text.replace("R", "").replace(",", "").strip()

    # Initialize an empty list to store the cleaned prices
    cleaned_prices = []

    price_float = float(price_elements)

    data = ("Studio 88", price_float)
    return data


def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    })

    data = [
        courtOrder(session),
        superbalist(session),
        studio88(session)
    ]
    print(courtOrder(session))
    print(superbalist(session))
    print(studio88(session))

    with orm.db_session:
        for item in data:
            Item(name=item[0], price=item[1], date_created=datetime.now())
        export_data_to_csv()


if __name__ == '__main__':
    main()
