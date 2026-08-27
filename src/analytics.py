import pandas as pd
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sales_clean.csv"


# ============================================================
# DATA LOADING
# ============================================================

def load_data():
    df = pd.read_csv(DATA_FILE)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================

def get_total_revenue():
    """Calculate total revenue."""
    df = load_data()
    return round(df["revenue"].sum(), 2)


def get_top_products(limit=5):
    """Return top products by revenue."""

    df = load_data()

    result = (
        df.groupby(
            ["product_id", "product_name"],
            as_index=False
        )["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_revenue_by_region():
    """Return revenue grouped by region."""

    df = load_data()

    result = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_revenue_by_category():
    """Return revenue grouped by category."""

    df = load_data()

    result = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_last_7_days_category_revenue():
    """Return category revenue for the latest 7 calendar days."""

    df = load_data()

    max_date = df["order_date"].max()
    start_date = max_date - pd.Timedelta(days=6)

    filtered = df[
        (df["order_date"] >= start_date)
        & (df["order_date"] <= max_date)
    ]

    result = (
        filtered.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    result["revenue"] = result["revenue"].round(2)

    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": max_date.strftime("%Y-%m-%d"),
        "categories": result.to_dict(orient="records"),
    }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
# Keep the original function names working as well.

def top_5_products():
    return get_top_products(5)


def revenue_by_region():
    return get_revenue_by_region()


def category_revenue_last_7_days():
    return get_last_7_days_category_revenue()


# ============================================================
# TEST / CLI
# ============================================================

if __name__ == "__main__":

    print("\n========== TOTAL REVENUE ==========")
    print(f"${get_total_revenue():,.2f}")

    print("\n========== TOP 5 PRODUCTS ==========")
    for item in get_top_products(5):
        print(
            item["product_name"],
            f"${item['revenue']:,.2f}"
        )

    print("\n========== REVENUE BY REGION ==========")
    for item in get_revenue_by_region():
        print(
            item["region"],
            f"${item['revenue']:,.2f}"
        )

    print("\n========== REVENUE BY CATEGORY ==========")
    for item in get_revenue_by_category():
        print(
            item["category"],
            f"${item['revenue']:,.2f}"
        )

    print("\n========== LAST 7 DAYS ==========")

    result = get_last_7_days_category_revenue()

    print(
        f"{result['start_date']} → "
        f"{result['end_date']}"
    )

    for item in result["categories"]:
        print(
            item["category"],
            f"${item['revenue']:,.2f}"
        )
