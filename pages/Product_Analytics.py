import streamlit as st
import requests
import pandas as pd

st.title(
    "Popular Products"
)

response = requests.get(
    "http://127.0.0.1:8000/popular-products"
)

data = response.json()

df = pd.DataFrame(data)

if len(df) > 0:

    st.dataframe(df)

    st.bar_chart(
        df.set_index(
            "product_name"
        )["clicks"]
    )

else:

    st.warning(
        "No product clicks yet."
    )