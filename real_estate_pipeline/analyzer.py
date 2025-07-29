import pandas as pd

MARKET_RENTS = {
    "Dubai Marina": 110000,
    "Downtown Dubai": 160000,
    "Jumeirah Village Circle": 70000,
    "Business Bay": 120000,
    "Palm Jumeirah": 220000,
}


def fill_missing_rent(row: pd.Series) -> float:
    """Fill missing rental price using market averages."""
    if pd.isna(row["rental_price"]):
        return MARKET_RENTS.get(row["location"], 0)
    return row["rental_price"]


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate financial metrics for each listing."""
    df = df.copy()
    df["rental_price"] = df.apply(fill_missing_rent, axis=1)

    df["annual_rent"] = df["rental_price"]
    df["price_to_rent_ratio"] = df["price"] / (df["annual_rent"])
    df["gross_yield"] = (df["annual_rent"] / df["price"]) * 100
    df["estimated_roi"] = df["gross_yield"] * 0.9  # assume 10% expenses
    df["break_even_years"] = 100 / df["estimated_roi"]
    return df


def filter_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    """Return filtered investment opportunities."""
    mask = (
        (df["price_to_rent_ratio"] < 15)
        & (df["gross_yield"] > 6)
        & (df["estimated_roi"] > 8)
    )
    return df[mask].sort_values(by="estimated_roi", ascending=False)
