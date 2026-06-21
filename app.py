import streamlit as st
import requests

st.title("WhatsApp Product Discovery Assistant")

query = st.text_input(
    "Enter Product Query"
)

if query:

    try:

        response = requests.post(
            "http://127.0.0.1:8000/rag-search",
            json={
                "query": query
            }
        )

        data = response.json()

        answer = data["answer"]

        results = data["products"]

        st.subheader(
            "AI Recommendation"
        )

        st.success(answer)

        st.subheader(
            "Recommended Products"
        )

        if len(results) > 0:

            for item in results:

                st.image(
                    item["image"],
                    width=250
                )

                st.write(
                    f"### {item['product']}"
                )

                st.write(
                    f"Category: {item['category']}"
                )

                st.write(
                    f"Color: {item['color']}"
                )

                st.write(
                    f"Material: {item['material']}"
                )

                st.write(
                    f"Price: ₹{item['price']}"
                )

                if st.button(
                    "View Product",
                    key=item["product"]
                ):

                    click_response = requests.post(
                        "http://127.0.0.1:8000/click",
                        json={
                            "product_name":
                            item["product"]
                        }
                    )

                    if click_response.status_code == 200:

                        st.success(
                            f"{item['product']} viewed successfully!"
                        )

                st.divider()

        else:

            st.warning(
                "No products found."
            )

    except Exception as e:

        st.error(
            f"API Error: {e}"
        )