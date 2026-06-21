import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_product_recommendation(
    query,
    products
):

    if not products:

        return (
            "Sorry, I couldn't find any matching products."
        )

    prompt = f"""
You are an AI shopping assistant.
All prices are in Indian Rupees (₹).

User Query:
{query}

Retrieved Products:
{products}

Recommend the most suitable products.

Recommend the best matching products.
Mention prices using ₹.
Do not use $.
Keep response under 100 words.
Return plain text only.

Do NOT use:
- markdown
- asterisks
- bullet symbols
- headings

Return plain text only.
"""

    response = model.generate_content(
        prompt
    )

    return response.text