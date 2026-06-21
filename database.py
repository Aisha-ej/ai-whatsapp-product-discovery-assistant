import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://aishan@localhost/luxury_products"

engine = create_engine(DATABASE_URL)


def get_products():

    query = """
    SELECT *
    FROM products
    """

    return pd.read_sql(
        query,
        engine
    )


def save_search(query):

    with engine.connect() as conn:

        conn.execute(
            text(
                """
                INSERT INTO search_history(query)
                VALUES(:query)
                """
            ),
            {"query": query}
        )

        conn.commit()


def get_search_history():

    query = """
    SELECT *
    FROM search_history
    ORDER BY searched_at DESC
    """

    return pd.read_sql(
        query,
        engine
    )

def save_product_click(product_name):

    with engine.connect() as conn:

        conn.execute(
            text(
                """
                INSERT INTO product_clicks(product_name)
                VALUES(:product_name)
                """
            ),
            {
                "product_name": product_name
            }
        )

        conn.commit()


def get_popular_products():

    query = """
    SELECT
        product_name,
        COUNT(*) as clicks
    FROM product_clicks
    GROUP BY product_name
    ORDER BY clicks DESC
    """

    return pd.read_sql(
        query,
        engine
    )

def get_recently_viewed():

    query = """
    SELECT
        product_name,
        clicked_at
    FROM product_clicks
    ORDER BY clicked_at DESC
    LIMIT 10
    """

    return pd.read_sql(
        query,
        engine
    )