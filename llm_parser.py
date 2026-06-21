from ollama import chat
import json
import re

def extract_filters_llm(query):

    prompt = f"""
You are a product search assistant.

Extract product filters from the query.

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT use comments.
- Do NOT explain anything.
- Use null for missing values.

Example:

{{
  "category": "Handbag",
  "color": "Black",
  "material": "Leather",
  "max_price": 2000
}}

Example 2:

Query: Need a purse below 2000

Output:

{{
  "category": "purse",
  "color": null,
  "material": null,
  "max_price": 2000
}}

Query:
{query}
"""

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"]

    print("\nRaw LLM Response:")
    print(content)

    try:
        # Extract JSON block
        match = re.search(r'\{.*?\}', content, re.DOTALL)

        if match:
            json_text = match.group(0)
            filters = json.loads(json_text)

            # Normalize list values from LLM
            for key, value in filters.items():

                if isinstance(value, list) and len(value) > 0:
                    filters[key] = value[0]
            print("\nNormalized Filters:")
            print(filters)

            return filters

        return {
            "error": "No JSON found",
            "raw_response": content
        }
    except Exception as e:
        return {
            "error": str(e),
            "raw_response": content
        }