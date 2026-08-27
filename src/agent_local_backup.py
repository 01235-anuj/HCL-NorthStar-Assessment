import pandas as pd
from pathlib import Path

from knowledge_base import search_documents


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sales_clean.csv"


# ============================================================
# DATA LOADING
# ============================================================

def load_data():
    """Load the cleaned sales dataset."""
    df = pd.read_csv(DATA_FILE)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


# ============================================================
# SALES ANALYTICS TOOLS
# ============================================================

def get_total_revenue():
    df = load_data()
    return round(df["revenue"].sum(), 2)


def get_top_products(limit=5):
    df = load_data()

    result = (
        df.groupby(["product_id", "product_name"], as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_revenue_by_region():
    df = load_data()

    result = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_revenue_by_category():
    df = load_data()

    result = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def get_last_7_days_category_revenue():
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
        "data": result.to_dict(orient="records"),
    }


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def get_knowledge_answer(question):
    """
    Search NorthStar policy/product documents and return
    a concise answer based on the most relevant document.
    """

    results = search_documents(question, top_k=1)

    if not results:
        return None

    result = results[0]
    source = result["source"]
    text = result["text"]

    q = question.lower()

    # --------------------------------------------------------
    # SHIPPING
    # --------------------------------------------------------

    if source == "shipping.json":

        if "express" in q and ("long" in q or "take" in q or "delivery" in q):
            return {
                "answer": (
                    "Express delivery arrives in 1 to 2 business days "
                    "regardless of region."
                ),
                "source": source,
            }

        if "standard" in q and "delivery" in q:
            return {
                "answer": (
                    "Standard delivery takes 3 to 5 business days "
                    "for same-region orders and 7 to 10 business days "
                    "for cross-region orders."
                ),
                "source": source,
            }

        if "track" in q:
            return {
                "answer": (
                    "A tracking link is emailed once the order ships, "
                    "usually within one business day of the order being placed."
                ),
                "source": source,
            }

    # --------------------------------------------------------
    # LOYALTY
    # --------------------------------------------------------

    if source == "loyalty.json":

        if "combined" in q or "combine" in q or "promotion" in q:
            return {
                "answer": (
                    "Yes. Loyalty points can be combined with seasonal "
                    "promotional pricing. They cannot be combined with "
                    "clearance pricing."
                ),
                "source": source,
            }

        if "point" in q and ("earn" in q or "work" in q):
            return {
                "answer": (
                    "Members earn 1 loyalty point for every 100 spent "
                    "on eligible purchases. Once 100 points are accumulated, "
                    "they can be redeemed for a discount voucher."
                ),
                "source": source,
            }

        if "expire" in q:
            return {
                "answer": (
                    "Unused loyalty points expire 18 months after they are earned. "
                    "Each batch of points has its own 18-month expiry period."
                ),
                "source": source,
            }

    # --------------------------------------------------------
    # SIZING
    # --------------------------------------------------------

    if source == "sizing.txt":

        if "denim" in q:
            return {
                "answer": (
                    "Denim jackets run approximately one size small compared "
                    "with the rest of the Apparel line. Customers close to "
                    "two sizes are generally advised to size up."
                ),
                "source": source,
            }

        if "size" in q or "sizing" in q:
            return {
                "answer": (
                    "NorthStar Apparel uses S, M, L, and XL sizing. "
                    "Customers should check the chest and waist measurements "
                    "on the individual product page."
                ),
                "source": source,
            }

    # --------------------------------------------------------
    # WARRANTY
    # --------------------------------------------------------

    if source == "warranty.pdf":

        if "period" in q or "long" in q:
            return {
                "answer": (
                    "The standard Electronics manufacturer warranty is "
                    "12 months from the date of purchase."
                ),
                "source": source,
            }

        if "covered" in q or "coverage" in q:
            return {
                "answer": (
                    "Warranty coverage includes component failures arising "
                    "under normal use that are not caused by damage, misuse, "
                    "or unauthorized modification."
                ),
                "source": source,
            }

    # --------------------------------------------------------
    # RETURN POLICY
    # --------------------------------------------------------

    if source == "returns.pdf":

        # Return window
        if "window" in q or "how long" in q:
            return {
                "answer": (
                    "The standard return window is 30 days from the Delivery Date."
                ),
                "source": source,
            }

        # After return window
        if (
            ("after" in q or "past" in q or "more than" in q)
            and ("30" in q or "thirty" in q or "day" in q)
        ):
            return {
                "answer": (
                    "The standard return window is 30 days from the Delivery Date, "
                    "so returns initiated after that window are generally outside "
                    "the standard return period."
                ),
                "source": source,
            }

        # Grocery returns
        if "grocery" in q:
            return {
                "answer": (
                    "No. Grocery items are not eligible for return under the "
                    "standard return policy."
                ),
                "source": source,
            }

        # Final Sale
        if "final sale" in q:
            return {
                "answer": (
                    "Products marked Final Sale at the time of purchase are not "
                    "eligible for return under the standard return policy."
                ),
                "source": source,
            }

        # Missing packaging / used items
        if (
            "packaging" in q
            or "used" in q
            or "condition" in q
        ):
            return {
                "answer": (
                    "Items that have been used beyond trying on or functional "
                    "testing, or that are missing original packaging, may still "
                    "be accepted at Support's discretion, but may receive a "
                    "reduced refund and a 10% restocking fee."
                ),
                "source": source,
            }

        # Refunds
        if "refund" in q:
            return {
                "answer": (
                    "Refunds are handled under NorthStar's Return and Refund "
                    "Policy. Items that do not meet standard condition "
                    "requirements may receive a reduced refund and may incur "
                    "a 10% restocking fee at Support's discretion."
                ),
                "source": source,
            }

        # Eligibility
        if "eligible" in q or "returnable" in q:
            return {
                "answer": (
                    "Most products are eligible for return within the standard "
                    "30-day return window, subject to the applicable condition "
                    "requirements. Grocery items and products marked Final Sale "
                    "are excluded."
                ),
                "source": source,
            }

        # General return question
        if "return" in q:
            return {
                "answer": (
                    "The standard return window is 30 days from the Delivery Date. "
                    "Grocery items and products marked Final Sale are excluded "
                    "from standard returns, and returned items must meet the "
                    "applicable condition requirements."
                ),
                "source": source,
            }

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return {
        "answer": text[:700].strip(),
        "source": source,
    }


# ============================================================
# LOCAL AGENT
# ============================================================

def answer_question(question):

    q = question.lower().strip()

    # --------------------------------------------------------
    # SALES QUESTIONS
    # --------------------------------------------------------

    if "total revenue" in q:
        revenue = get_total_revenue()

        return f"Total revenue is ${revenue:,.2f}."

    if "top" in q and "product" in q:
        products = get_top_products(5)

        answer = "Top products by revenue:\n"

        for i, product in enumerate(products, 1):
            answer += (
                f"{i}. {product['product_name']} "
                f"(${product['revenue']:,.2f})\n"
            )

        return answer.rstrip()

    if (
        "highest revenue" in q
        and "region" in q
    ) or (
        "highest revenue region" in q
    ):
        regions = get_revenue_by_region()

        if regions:
            top = regions[0]

            return (
                f"{top['region']} has the highest revenue "
                f"at ${top['revenue']:,.2f}."
            )

    if "region" in q and "revenue" in q:
        regions = get_revenue_by_region()

        answer = "Revenue by region:\n"

        for region in regions:
            answer += (
                f"- {region['region']}: "
                f"${region['revenue']:,.2f}\n"
            )

        return answer.rstrip()

    if (
        "most revenue" in q
        and "product" in q
    ) or (
        "highest revenue" in q
        and "product" in q
    ):
        products = get_top_products(1)

        if products:
            product = products[0]

            return (
                f"{product['product_name']} generated the "
                f"highest revenue at "
                f"${product['revenue']:,.2f}."
            )

    if "revenue of" in q:
        products = get_top_products(100)

        for product in products:
            product_name = product["product_name"].lower()

            if product_name in q:
                return (
                    f"{product['product_name']} generated "
                    f"${product['revenue']:,.2f} in revenue."
                )

    if "last 7" in q or "last seven" in q:

        result = get_last_7_days_category_revenue()

        answer = (
            f"Category revenue from "
            f"{result['start_date']} to "
            f"{result['end_date']}:\n"
        )

        for item in result["data"]:
            answer += (
                f"- {item['category']}: "
                f"${item['revenue']:,.2f}\n"
            )

        return answer.rstrip()

    if "category" in q and "revenue" in q:

        categories = get_revenue_by_category()

        answer = "Revenue by category:\n"

        for category in categories:
            answer += (
                f"- {category['category']}: "
                f"${category['revenue']:,.2f}\n"
            )

        return answer.rstrip()

    # --------------------------------------------------------
    # KNOWLEDGE / POLICY QUESTIONS
    # --------------------------------------------------------

    knowledge = get_knowledge_answer(question)

    if knowledge:

        return (
            f"{knowledge['answer']}\n\n"
            f"Source: {knowledge['source']}"
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return (
        "I could not find enough information to answer that. "
        "I can answer sales analytics questions and questions "
        "about NorthStar Retail policies and product documents."
    )


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("      NORTHSTAR SALES DATA AGENT")
    print("========================================")

    print("\nDataset:", DATA_FILE)

    df = load_data()

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nAgent ready.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        print("\nAgent:")

        try:
            print(answer_question(question))
        except Exception as e:
            print("Error:", type(e).__name__, "-", e)

        print()
