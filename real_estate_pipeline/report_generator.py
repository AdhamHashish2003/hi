import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class ReportGenerator:
    """Generate Excel and PDF reports from listing data."""

    def __init__(self, out_dir: str = "reports"):
        self.out_dir = out_dir

    def _ensure_out_dir(self):
        import os

        os.makedirs(self.out_dir, exist_ok=True)

    def generate(self, df: pd.DataFrame) -> str:
        """Create Excel report with charts."""
        self._ensure_out_dir()
        date_str = datetime.now().strftime("%Y-%m-%d")
        excel_path = f"{self.out_dir}/dubai_report_{date_str}.xlsx"
        pdf_path = f"{self.out_dir}/dubai_report_{date_str}.pdf"

        with pd.ExcelWriter(excel_path) as writer:
            df.to_excel(writer, index=False, sheet_name="All Listings")

            # Summary of top opportunities
            df.head(20).to_excel(writer, index=False, sheet_name="Top Deals")

        # Charts
        plt.figure(figsize=(10, 6))
        df.groupby("location")["gross_yield"].mean().plot(kind="bar")
        plt.ylabel("Average Gross Yield %")
        plt.title("Yield by Neighborhood")
        plt.tight_layout()
        plt.savefig(f"{self.out_dir}/yield_by_location.png")
        plt.close()

        plt.figure(figsize=(10, 6))
        df["price"].divide(df["sqft"]).plot(kind="hist", bins=20)
        plt.xlabel("Price per sqft (AED)")
        plt.title("Distribution of Price per sqft")
        plt.tight_layout()
        plt.savefig(f"{self.out_dir}/price_per_sqft.png")
        plt.close()

        plt.figure(figsize=(10, 6))
        years = range(1, 6)
        roi_values = []
        for year in years:
            roi_values.append(((1 + df["estimated_roi"] / 100) ** year - 1) * 100)
        plt.plot(years, roi_values)
        plt.xlabel("Years")
        plt.ylabel("ROI %")
        plt.title("ROI Projection Over 5 Years")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{self.out_dir}/roi_projection.png")
        plt.close()

        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Dubai Real Estate Investment Report", 0, 1)
            pdf.image(f"{self.out_dir}/yield_by_location.png", w=180)
            pdf.add_page()
            pdf.image(f"{self.out_dir}/price_per_sqft.png", w=180)
            pdf.add_page()
            pdf.image(f"{self.out_dir}/roi_projection.png", w=180)
            pdf.output(pdf_path)
        except Exception:
            pass

        return excel_path
