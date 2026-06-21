import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from llm_parser import extract_filters_llm
from vector_search.search_products import semantic_search
#from search_products import semantic_search

def is_structured_query(filters):

    useful_fields = [
        "category",
        "color",
        "material",
        "max_price"
    ]

    count = 0

    for field in useful_fields:

        if field in filters and filters[field]:
            count += 1

    return count >= 2


query = input("Enter Query: ")

filters = extract_filters_llm(query)

print("\nExtracted Filters:")
print(filters)

if "error" not in filters and is_structured_query(filters):

    print("\nUsing Structured Search")

else:

    print("\nUsing Semantic Search")

    semantic_search(query)