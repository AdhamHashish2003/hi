import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional


class ListingScraper:
    """Scrapes real estate listings or loads sample data."""

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0 Safari/537.36"
    )

    def __init__(self, sample_path: str = "sample_data.csv"):
        self.sample_path = os.path.join(os.path.dirname(__file__), sample_path)

    def fetch_listings(self) -> pd.DataFrame:
        """Fetch listings from target sites. Returns dataframe."""
        try:
            listings = []
            headers = {"User-Agent": self.USER_AGENT}
            # Example: scraping a site like Bayut (simplified, may break)
            url = "https://www.bayut.com/for-sale/property/dubai/"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("article")
            for card in cards:
                try:
                    loc = card.select_one("[data-testid=location]").get_text(strip=True)
                    price = (
                        card.select_one("[data-testid=price]")
                        .get_text(strip=True)
                        .replace(",", "")
                        .replace("AED", "")
                    )
                    details = card.select("span")
                    bedrooms = bathrooms = sqft = None
                    for d in details:
                        text = d.get_text()
                        if "Bed" in text:
                            bedrooms = int(text.split()[0])
                        elif "Bath" in text:
                            bathrooms = int(text.split()[0])
                        elif "sqft" in text:
                            sqft = float(text.replace(",", "").split()[0])
                    listings.append(
                        {
                            "location": loc,
                            "price": float(price),
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                            "sqft": sqft,
                            "furnishing": None,
                            "listing_type": "Sale",
                            "rental_price": None,
                        }
                    )
                except Exception:
                    continue
            if not listings:
                raise ValueError("No listings scraped")
            return pd.DataFrame(listings)
        except Exception:
            # Fallback to sample data
            return pd.read_csv(self.sample_path)

    def geocode_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optional geocoding using Google Maps API."""
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            return df
        try:
            import googlemaps

            gmaps = googlemaps.Client(key=api_key)
            latitudes = []
            longitudes = []
            for loc in df["location"]:
                try:
                    geocode_result = gmaps.geocode(f"{loc}, Dubai, UAE")
                    if geocode_result:
                        lat = geocode_result[0]["geometry"]["location"]["lat"]
                        lng = geocode_result[0]["geometry"]["location"]["lng"]
                    else:
                        lat = lng = None
                except Exception:
                    lat = lng = None
                latitudes.append(lat)
                longitudes.append(lng)
            df = df.copy()
            df["latitude"] = latitudes
            df["longitude"] = longitudes
            return df
        except Exception:
            # If geocoding fails, return without coordinates
            return df
