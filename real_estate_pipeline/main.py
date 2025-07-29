from scraper import ListingScraper
from analyzer import compute_metrics, filter_opportunities
from report_generator import ReportGenerator


def run_pipeline():
    scraper = ListingScraper()
    df = scraper.fetch_listings()
    df = scraper.geocode_properties(df)
    df = compute_metrics(df)
    opportunities = filter_opportunities(df)
    report = ReportGenerator()
    path = report.generate(opportunities)
    print(f"Report generated at {path}")


if __name__ == "__main__":
    run_pipeline()
