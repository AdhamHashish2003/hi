# Investment Tracker

This is a simple web page that allows you to track the current value of an investment. Enter the asset ID (as used on CoinGecko), the price you bought it at in USD, and the number of units. The page fetches the latest price and calculates your current value and profit/loss.

## Usage

Open `index.html` in a web browser. Fill in the form with your asset information and click **Track** to retrieve the latest price.

## Real Estate Bot

A simple script `real_estate_bot.py` demonstrates how you might analyze Dubai real estate investments. It uses a dataset `dubai_real_estate.csv` generated from multiple listing pages and a basic linear regression (implemented without external libraries) to estimate return on investment (ROI). The script prints the top ten properties with the highest predicted ROI.

To build the dataset from several listing pages (or example HTML files), run:

```bash
python3 scrape_dubai_listings.py
```

This combines all listings into `dubai_real_estate.csv`. The resulting CSV
includes a `listing_url` column pointing to the page where each property was
found.

Run the bot with:

```bash
python3 real_estate_bot.py
```

The bot prints the top 10 properties along with the URL where each listing was
scraped.

The dataset is illustrative only; replace it with real data to perform meaningful analysis.
