from analytics import (
    get_total_revenue,
    get_top_products,
    get_revenue_by_region,
    get_revenue_by_category,
    get_last_7_days_category_revenue,
)


def money(value):
    return f"${value:,.2f}"


def answer_question(question):
    q = question.lower().strip()

    # --------------------------------------------------------
    # TOTAL REVENUE
    # --------------------------------------------------------
    if "total revenue" in q:
        total = get_total_revenue()
        return f"Total revenue is {money(total)}."

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------
    if (
        "top 5 products" in q
        or "top five products" in q
        or "best 5 products" in q
        or "highest revenue products" in q
    ):
        products = get_top_products(5)

        lines = ["Top products by revenue:"]
        for i, row in enumerate(products, 1):
            lines.append(
                f"{i}. {row['product_name']} "
                f"({money(row['revenue'])})"
            )

        return "\n".join(lines)

    # --------------------------------------------------------
    # HIGHEST REVENUE PRODUCT
    # --------------------------------------------------------
    if (
        "which product" in q
        and ("most revenue" in q or "highest revenue" in q)
    ):
        products = get_top_products(1)

        if products:
            p = products[0]
            return (
                f"{p['product_name']} generated the highest revenue "
                f"at {money(p['revenue'])}."
            )

    # --------------------------------------------------------
    # REVENUE BY REGION
    # --------------------------------------------------------
    if "revenue by region" in q or "revenue by regions" in q:
        regions = get_revenue_by_region()

        lines = ["Revenue by region:"]
        for row in regions:
            lines.append(
                f"- {row['region']}: {money(row['revenue'])}"
            )

        return "\n".join(lines)

    # --------------------------------------------------------
    # HIGHEST REVENUE REGION
    # --------------------------------------------------------
    if (
        "which region" in q
        and ("highest revenue" in q or "most revenue" in q)
    ):
        regions = get_revenue_by_region()

        if regions:
            top = max(regions, key=lambda x: x["revenue"])
            return (
                f"{top['region']} has the highest revenue "
                f"at {money(top['revenue'])}."
            )

    # --------------------------------------------------------
    # LAST 7 DAYS
    # IMPORTANT: Check this BEFORE generic category revenue
    # --------------------------------------------------------
    if (
        "last 7 days" in q
        or "last seven days" in q
        or "past 7 days" in q
        or "past seven days" in q
    ):
        data = get_last_7_days_category_revenue()

        lines = []

        if isinstance(data, dict) and "start_date" in data:
            lines.append(
                f"Category revenue from "
                f"{data['start_date']} to {data['end_date']}:"
            )
            categories = data["categories"]

        else:
            categories = data
            lines.append("Category revenue for the latest 7 days:")

        for row in categories:
            lines.append(
                f"- {row['category']}: {money(row['revenue'])}"
            )

        return "\n".join(lines)

    # --------------------------------------------------------
    # REVENUE BY CATEGORY
    # --------------------------------------------------------
    if (
        "revenue by category" in q
        or "revenue by categories" in q
        or "category revenue" in q
    ):
        categories = get_revenue_by_category()

        lines = ["Revenue by category:"]
        for row in categories:
            lines.append(
                f"- {row['category']}: {money(row['revenue'])}"
            )

        return "\n".join(lines)

    # --------------------------------------------------------
    # SPECIFIC PRODUCT REVENUE
    # --------------------------------------------------------
    products = get_top_products(1000)

    for row in products:
        product_name = row["product_name"].lower()

        if product_name in q:
            return (
                f"{row['product_name']} generated "
                f"{money(row['revenue'])} in revenue."
            )

    # --------------------------------------------------------
    # UNKNOWN QUESTION
    # --------------------------------------------------------
    return (
        "I can answer questions about total revenue, top products, "
        "revenue by region, revenue by category, last 7 days category "
        "revenue, and individual product revenue."
    )


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("      NORTHSTAR SALES DATA AGENT")
    print("=" * 50)

    print("\nDataset: data/sales_clean.csv")

    print("\nAgent ready.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            answer = answer_question(question)

            print("\nAgent:")
            print(answer)
            print()

        except Exception as e:
            print("\nAgent error:")
            print(type(e).__name__, "-", e)
            print()
