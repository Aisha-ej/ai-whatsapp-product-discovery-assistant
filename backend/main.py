from fastapi import FastAPI
from models import QueryRequest
from search_service import search_products
from analytics import analytics_data
from database import save_product_click,get_popular_products,get_recently_viewed
from whatsapp import router as whatsapp_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from rag_generator import generate_product_recommendation

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/images",
    StaticFiles(directory=str(BASE_DIR / "Images")
    ),
    name="images"
)

app.include_router(
    whatsapp_router
)

@app.get("/")
def home():

    return {
        "message": "WhatsApp Product Discovery API"
    }

@app.post("/search")
def search(request: QueryRequest):

    print("API Called")
    print(request.query)

    results = search_products(
        request.query
    )

    return results

@app.post("/rag-search")
def rag_search(request: QueryRequest):

    products = search_products(
        request.query
    )

    answer = generate_product_recommendation(
        request.query,
        products
    )

    return {
        "answer": answer,
        "products": products
    }

@app.get("/analytics")
def analytics():

    return analytics_data()

@app.post("/click")
def product_click(data: dict):

    save_product_click(
        data["product_name"]
    )

    return {
        "message": "Click saved"
    }

@app.get("/popular-products")
def popular_products():

    df = get_popular_products()

    return df.to_dict(
        orient="records"
    )

@app.get("/recently-viewed")
def recently_viewed():

    df = get_recently_viewed()

    return df.to_dict(
        orient="records"
    )


