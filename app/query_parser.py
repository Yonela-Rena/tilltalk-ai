import json
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_query(query):
    """
    Convert a cashier's natural-language request
    into structured product information.
    """

    prompt = f"""
You are the query-understanding component of TillTalk,
an AI assistant for supermarket cashiers.

Extract the following information from the cashier's request:

1. product_name
2. brand
3. size

Rules:
- Return null when a value is not mentioned.
- Do not invent information.
- Keep the product name concise.
- Keep the size exactly as stated when possible.

Cashier request:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "product_name": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "brand": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "size": {
                        "type": "STRING",
                        "nullable": True
                    }
                },
                "required": [
                    "product_name",
                    "brand",
                    "size"
                ]
            }
        }
    )

    return json.loads(response.text)