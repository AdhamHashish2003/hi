"""Scrape multiple Dubai real estate listing pages and combine them into a CSV.
This example uses local HTML files but works with HTTP URLs as well.
"""

import csv
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import urlopen

FIELDS = [
    "property_id",
    "location",
    "bedrooms",
    "size_sqft",
    "price",
    "rental_income",
    "property_type",
]


class ListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.listings = []

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            return
        attr = dict(attrs)
        if attr.get("class") != "listing":
            return
        self.listings.append(
            {
                "property_id": attr.get("data-id", ""),
                "location": attr.get("data-location", ""),
                "bedrooms": attr.get("data-bedrooms", "0"),
                "size_sqft": attr.get("data-size", "0"),
                "price": attr.get("data-price", "0"),
                "rental_income": attr.get("data-rental", "0"),
                "property_type": attr.get("data-type", ""),
            }
        )


def fetch_content(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        with urlopen(url) as resp:
            return resp.read().decode()
    else:
        with open(url, "r") as f:
            return f.read()


def scrape_urls(urls, output_csv="dubai_real_estate.csv"):
    all_rows = []
    for url in urls:
        html = fetch_content(url)
        parser = ListingParser()
        parser.feed(html)
        all_rows.extend(parser.listings)

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    return all_rows


if __name__ == "__main__":
    # Replace these with real URLs when available
    urls = ["site1.html", "site2.html"]
    scraped = scrape_urls(urls)
    print(f"Wrote {len(scraped)} listings to dubai_real_estate.csv")
