from scraper import ListingScraper
from analyzer import compute_metrics, filter_opportunities
from report_generator import ReportGenerator
from web_report import generate_html


def run_pipeline():
    scraper = ListingScraper()
    df = scraper.fetch_listings()
    df = scraper.geocode_properties(df)
    df = compute_metrics(df)
    opportunities = filter_opportunities(df)
    report = ReportGenerator()
    path = report.generate(opportunities)
    print(f"Report generated at {path}")
    html_path = generate_html(opportunities)
    print(f"HTML report generated at {html_path}")


if __name__ == "__main__":
    run_pipeline()
