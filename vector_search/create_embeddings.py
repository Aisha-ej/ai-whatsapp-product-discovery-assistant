#Generate embeddings
import pandas as pd
import chromadb
import ollama

# Load products
df = pd.read_csv("products.csv")

# Create Chroma client
client = chromadb.PersistentClient(path="./chroma_db_v2")

# Create collection
collection = client.get_or_create_collection(
    name="products"
)

# Remove old records
try:
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])
except:
    pass

for index, row in df.iterrows():

    description = f"""
    Product: {row['Product']}
    Category: {row['Category']}
    Color: {row['Color']}
    Material: {row['Material']}
    Price: {row['Price']}
    """

    embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=description
    )["embedding"]

    collection.add(
        ids=[str(index)],
        embeddings=[embedding],
        documents=[description],
        metadatas=[{
            "product": row["Product"],
            "category": row["Category"],
            "color": row["Color"],
            "material": row["Material"],
            "price": int(row["Price"]),
            "image": row["Image"]
        }]
    )

print("Embeddings created successfully!")