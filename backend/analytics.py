from database import get_search_history


def analytics_data():

    history = get_search_history()

    top_searches = (
        history["query"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_searches.columns = [
        "query",
        "count"
    ]

    history["date"] = (
        history["searched_at"]
        .dt.date
    )

    searches_per_day = (
        history.groupby("date")
        .size()
        .reset_index(name="count")
    )

    return {
        "total_searches": len(history),

        "recent_searches":
        history.head(10).to_dict(
            orient="records"
        ),

        "top_searches":
        top_searches.to_dict(
            orient="records"
        ),

        "searches_per_day":
        searches_per_day.to_dict(
            orient="records"
        )
    }