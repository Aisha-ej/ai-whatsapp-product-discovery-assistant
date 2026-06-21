import streamlit as st
import requests
import pandas as pd

st.title(
    "Recently Viewed Products"
)

response = requests.get(
    "http://127.0.0.1:8000/recently-viewed"
)

data = response.json()

if len(data) > 0:

    df = pd.DataFrame(data)

    st.dataframe(df)

else:

    st.warning(
        "No viewed products yet."
    )