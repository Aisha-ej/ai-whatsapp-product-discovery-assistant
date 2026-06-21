import streamlit as st
import requests
import pandas as pd

st.title("Search Analytics")

response = requests.get(
    "http://127.0.0.1:8000/analytics"
)

data = response.json()

st.metric(
    "Total Searches",
    data["total_searches"]
)

st.subheader("Recent Searches")

for item in data["recent_searches"]:

    st.write(item["query"])

st.divider()

st.subheader("Top Searches")

for item in data["top_searches"]:

    st.write(
        f"{item['query']} ({item['count']})"
    )

st.divider()

st.subheader(
    "Search Trends"
)

trend_df = pd.DataFrame(
    data["searches_per_day"]
)

if len(trend_df) > 0:

    trend_df = trend_df.set_index(
        "date"
    )

    st.line_chart(
        trend_df["count"]
    )