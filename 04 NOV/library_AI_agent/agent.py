
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import search_books, reserve_book


# Load API key from .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")


# Connect to OpenRouter
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openrouter/free"


# Define tools for the AI model
TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": (
                "Search for books using a title, keyword, author "
                "or category. Use this when the user wants to find "
                "books or check book availability."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Book title, keyword, author or category"
                    }
                },
                "required": ["keyword"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": (
                "Reserve a book using its ID and customer name. "
                "If the user gives a book title, search for the book "
                "first to obtain its ID. Check availability before "
                "attempting the reservation. The Python tool will "
                "ask the user for confirmation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "Unique ID of the book"
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Name of the customer"
                    }
                },
                "required": ["book_id", "customer_name"]
            }
        }
    }

]


# Map tool names to Python functions
available_functions = {
    "search_books": search_books,
    "reserve_book": reserve_book
}


# AI Agent
def run_agent(user_input):

    messages = [

        {
            "role": "system",
            "content": """
            You are an AI Library Assistant.

            You help users search for books and reserve books.

            Rules:

            1. Use search_books whenever the user asks to
               find books or check availability.

            2. If the user wants to reserve a book by title,
               search for it first to obtain its book ID.

            3. Use reserve_book for reservation requests.

            4. Never invent book IDs or book availability.

            5. If a book is unavailable, explain that it
               cannot be reserved.

            6. The Python reservation tool asks for user
               confirmation. Do not claim a reservation
               succeeded unless the tool confirms success.

            7. Give clear and friendly responses.
            """
        },

        {
            "role": "user",
            "content": user_input
        }

    ]

    # Allow multiple tool calls in one agent interaction
    for _ in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        # Check whether the AI selected a tool
        if assistant_message.tool_calls:

            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("\nSelected Tool:", function_name)
                print("Arguments:", arguments)

                # Execute the selected Python function
                function_to_call = available_functions.get(
                    function_name
                )

                if function_to_call is None:
                    result = {"status": "error",
                              "message": "Unknown tool."}
                else:
                    result = function_to_call(**arguments)

                print("Tool Result:", result)

                # Send the tool result back to the AI model
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        else:

            # Display the final AI response
            print("\nAI Library Assistant:")
            print(assistant_message.content)

            return

    print("\nAgent stopped after maximum tool-call rounds.")


# Main program
if __name__ == "__main__":

    print("     AI LIBRARY ASSISTANT")

    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Thank you for using the Library Assistant!")
            break

        if not user_input:
            continue

        try:
            run_agent(user_input)

        except Exception as e:
            print("\nError:", e)
