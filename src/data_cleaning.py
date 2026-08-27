import pandas as pd
from pathlib import Path


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "sales.csv"
CLEAN_FILE = BASE_DIR / "data" / "sales_clean.csv"


# =========================
# LOAD DATA
# =========================

df = pd.read_csv(RAW_FILE)

print("========== RAW DATA ==========")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# =========================
# 1. NORMALIZE DATE
# =========================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    errors="coerce"
)

invalid_dates = df["order_date"].isna().sum()

print("\n========== DATE CLEANING ==========")
print(f"Unparseable dates: {invalid_dates}")

# We do not remove the slash-format dates because
# they are valid dates represented differently.

df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")


# =========================
# 2. RECOVER PRODUCT NAMES
# =========================

product_name_map = (
    df.dropna(subset=["product_name"])
      .drop_duplicates("product_id")
      .set_index("product_id")["product_name"]
)

missing_product_names = df["product_name"].isna().sum()

df["product_name"] = (
    df["product_name"]
    .fillna(df["product_id"].map(product_name_map))
)

remaining_product_names = df["product_name"].isna().sum()

print("\n========== PRODUCT NAME CLEANING ==========")
print(f"Missing before: {missing_product_names}")
print(f"Recovered: {missing_product_names - remaining_product_names}")
print(f"Remaining missing: {remaining_product_names}")


# =========================
# 3. RECOVER UNIT PRICES
# =========================

price_map = (
    df.dropna(subset=["unit_price"])
      .groupby("product_id")["unit_price"]
      .first()
)

missing_prices = df["unit_price"].isna().sum()

df["unit_price"] = (
    df["unit_price"]
    .fillna(df["product_id"].map(price_map))
)

remaining_prices = df["unit_price"].isna().sum()

print("\n========== UNIT PRICE CLEANING ==========")
print(f"Missing before: {missing_prices}")
print(f"Recovered: {missing_prices - remaining_prices}")
print(f"Remaining missing: {remaining_prices}")


# =========================
# 4. REMOVE INVALID QUANTITY
# =========================

missing_quantity = df["quantity"].isna().sum()
negative_quantity = (df["quantity"] < 0).sum()

before_quantity_filter = len(df)

df = df[
    df["quantity"].notna() &
    (df["quantity"] > 0)
].copy()

removed_quantity_rows = before_quantity_filter - len(df)

print("\n========== QUANTITY CLEANING ==========")
print(f"Missing quantity: {missing_quantity}")
print(f"Negative quantity: {negative_quantity}")
print(f"Rows removed: {removed_quantity_rows}")


# =========================
# 5. REMOVE EXACT DUPLICATES
# =========================

before_duplicates = len(df)

exact_duplicates = df.duplicated().sum()

df = df.drop_duplicates().copy()

removed_duplicates = before_duplicates - len(df)

print("\n========== DUPLICATE CLEANING ==========")
print(f"Exact duplicate rows: {exact_duplicates}")
print(f"Rows removed: {removed_duplicates}")


# =========================
# 6. CALCULATE REVENUE
# =========================

df["revenue"] = df["quantity"] * df["unit_price"]


# =========================
# 7. FINAL VALIDATION
# =========================

print("\n========== FINAL VALIDATION ==========")

print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nMissing values:")
print(df.isna().sum())

print("\nInvalid quantity:")
print((df["quantity"] <= 0).sum())

print("\nInvalid unit price:")
print((df["unit_price"] <= 0).sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDate range:")
print("Min:", df["order_date"].min())
print("Max:", df["order_date"].max())


# =========================
# 8. SAVE CLEAN DATA
# =========================

df.to_csv(CLEAN_FILE, index=False)

print("\n========== OUTPUT ==========")
print(f"Clean dataset saved to: {CLEAN_FILE}")