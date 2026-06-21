import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from llm_parser import extract_filters_llm
from database import get_products, save_search
from vector_search.search_products import semantic_search


def normalize_category(category):

    if not category:
        return None

    category = str(category).lower()

    if category in [
        "bag",
        "bags",
        "handbag",
        "handbags",
        "purse",
        "purses"
    ]:
        return "Handbag"

    elif category in [
        "wallet",
        "wallets"
    ]:
        return "Wallet"

    elif category in [
        "clutch",
        "clutches"
    ]:
        return "Clutch"

    return None


def is_structured_query(filters):

    valid_categories = [
        "Handbag",
        "Wallet",
        "Clutch"
    ]

    if (
        filters.get("category")
        and filters["category"] in valid_categories
    ):
        return True

    if filters.get("max_price"):
        return True

    return False


def search_products(query):

    save_search(query)

    products = get_products()

    # =====================================
    # EXACT / PARTIAL PRODUCT NAME SEARCH
    # =====================================

    product_match = products[
        products["product"].str.lower().str.contains(
            query.lower(),
            na=False
        )
    ]

    if len(product_match) > 0:

        print("\nUsing Product Name Search")

        return product_match.to_dict(
            orient="records"
        )

    # =====================================
    # LLM FILTER EXTRACTION
    # =====================================

    filters = extract_filters_llm(query)

    if filters.get("category"):

        filters["category"] = normalize_category(
            filters["category"]
        )

    print("\nNormalized Filters:")
    print(filters)

    # =====================================
    # STRUCTURED SEARCH
    # =====================================

    if is_structured_query(filters):

        print("\nUsing Structured Search")

        print("\nAll Products:")
        print(products)

        if filters.get("category"):

            products = products[
                products["category"].str.lower()
                == str(filters["category"]).lower()
            ]

        if filters.get("color"):

            products = products[
                products["color"].str.lower()
                == str(filters["color"]).lower()
            ]

        if filters.get("material"):

            products = products[
                products["material"].str.lower()
                == str(filters["material"]).lower()
            ]

        if filters.get("max_price"):

            products = products[
                products["price"]
                <= filters["max_price"]
            ]

        if len(products) == 0:

            print(
                "\nNo structured results. Using semantic search."
            )

            return semantic_search(query)

        return products.to_dict(
            orient="records"
        )

    # =====================================
    # SEMANTIC SEARCH
    # =====================================

    print("\nUsing Semantic Search")

    return semantic_search(query)