# Investment Tracker and Real Estate Pipeline

This repository contains a simple investment tracker web page as well as a Python-based data pipeline for analyzing Dubai real estate opportunities.

## Web Page
Open `index.html` in a web browser. Fill in the form with your asset information and click **Track** to retrieve the latest price.

## Dubai Real Estate Pipeline
The `real_estate_pipeline` package provides tools to scrape or load sample Dubai property listings, calculate key financial metrics, and generate a daily investment report.

### Running the Pipeline
Ensure Python 3.8+ is installed. Install dependencies:

```bash
pip install pandas beautifulsoup4 requests matplotlib fpdf googlemaps
```

Set the `GOOGLE_MAPS_API_KEY` environment variable if you want the pipeline to
geocode properties.

Then run:

```bash
python -m real_estate_pipeline.main
```

A report will be generated in the `reports/` directory. If scraping is blocked, sample data will be used automatically.
The pipeline also writes an `index.html` file with property links and images for quick browsing.
