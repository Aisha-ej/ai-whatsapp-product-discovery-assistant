import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("products.csv")

# Convert columns to lowercase
df.columns = [col.lower() for col in df.columns]

engine = create_engine(
    "postgresql://localhost/luxury_products"
)

df.to_sql(
    "products",
    engine,
    if_exists="replace",
    index=False
)

print("Products loaded successfully!")