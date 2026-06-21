from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from rag_generator import generate_product_recommendation

from search_service import search_products

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):

    form_data = await request.form()

    query = (form_data.get("Body") or "").strip().lower()

    print("=" * 50)
    print("Incoming WhatsApp Query:", query)
    print("=" * 50)

    response = MessagingResponse()

    # Greetings
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if query in greetings:

        response.message(
            "👋 Hello! Welcome to Product Discovery Assistant.\n\n"
            "I can help you find products.\n\n"
            "Try:\n"
            "• Show me black handbags\n"
            "• Leather wallet under 1000\n"
            "• Gold clutch\n"
            "• Black leather handbags under 2000\n"
            "• Red Bag"
        )

        print("GREETING RESPONSE:")
        print(str(response))

        return Response(
            content=str(response),
            media_type="application/xml; charset=utf-8"
        )

    # Help command
    if query == "help":

        response.message(
            "📌 Available Commands:\n\n"
            "• Show me black handbags\n"
            "• Leather wallet under 1000\n"
            "• Gold clutch\n"
            "• Black leather handbags under 2000\n"
            "• Red Bag\n\n"
            "Simply describe the product you're looking for."
        )

        return Response(
            content=str(response),
            media_type="application/xml; charset=utf-8"
        )

    # Search products
    results = search_products(query)

    rag_answer = generate_product_recommendation(
    query,
    results
    )
    
    print("=" * 50)
    print("RAG ANSWER:")
    print(rag_answer)
    print("=" * 50)

    print("QUERY:", query)
    print("RESULTS:", results)

    print("=" * 50)
    print("RESULT TYPE:", type(results))
    print("RESULTS:", results)
    print("=" * 50)

    if results and len(results) > 0:

            # Message 1: Gemini recommendation
            response.message(rag_answer)

            # Message 2: Best product only
            best_product = results[0]

            image_url = (
                "https://agreement-varying-humpback.ngrok-free.dev/images/"
                + best_product["image"].split("/")[-1]
            )

            msg = response.message()

            msg.body(
                f"👜 {best_product['product']}\n"
                f"Category: {best_product['category']}\n"
                f"Color: {best_product['color']}\n"
                f"Material: {best_product['material']}\n"
                f"Price: ₹{best_product['price']}"
            )

            msg.media(image_url)
            print("FINAL TWIML:")
            print(str(response))

    else:

        response.message(
            "😕 No matching products found.\n\n"
            "Try searching like:\n"
            "• Black handbag\n"
            "• Leather wallet\n"
            "• Red clutch"
        )

    return Response(
        content=str(response),
        media_type="application/xml; charset=utf-8"
    )