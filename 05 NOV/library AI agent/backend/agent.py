
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import search_books, reserve_book

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openrouter/free"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Search books by title, keyword, author or category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": "Reserve a book using its ID and customer name. Search by title first if needed. The function returns a confirmation request before creating the reservation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "integer"},
                    "customer_name": {"type": "string"}
                },
                "required": ["book_id", "customer_name"]
            }
        }
    }
]

FUNCTIONS = {
    "search_books": search_books,
    "reserve_book": reserve_book
}


def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": """
            You are an AI Library Assistant.

            Help users search and reserve books.

            Rules:
            - Use search_books to find books and check availability.
            - For reservations, search by title first if the ID is unknown.
            - Use reserve_book to request a reservation.
            - Never invent book IDs or availability.
            - If confirmation is required, tell the user
              that they must approve the reservation.
            - Never claim a reservation succeeded unless
              the tool returns success.
            - Be friendly and concise.
            """
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    tools_used = []
    pending_reservation = None

    for _ in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        if not assistant_message.tool_calls:

            return {
                "reply": assistant_message.content or
                         "I couldn't generate a response.",
                "tools_used": tools_used,
                "pending_reservation": pending_reservation
            }

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name
            arguments = json.loads(
                tool_call.function.arguments
            )

            tools_used.append(function_name)

            function_to_call = FUNCTIONS.get(function_name)

            if function_to_call is None:
                result = {
                    "status": "error",
                    "message": "Unknown tool."
                }
            else:
                result = function_to_call(**arguments)

            if result.get("status") == "confirmation_required":
                pending_reservation = result

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return {
        "reply": "I couldn't complete the request. Please try again.",
        "tools_used": tools_used,
        "pending_reservation": pending_reservation
    }
